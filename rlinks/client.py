###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Crossbar.io Technologies GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

import sys
import copy
import uuid
import os
import argparse
import hashlib
import binascii
import configparser
from pprint import pprint

import txaio
from zlmdb import time_ns

from twisted.internet.defer import inlineCallbacks, gatherResults
from twisted.internet.task import LoopingCall, react

from autobahn.wamp.exception import TransportLost
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.types import SubscribeOptions, PublishOptions, RegisterOptions, CallOptions
from crossbar.common.processinfo import ProcessInfo
from crossbar._util import hl


class HATestClientSession(ApplicationSession):

    TEST_TOPIC = 'com.example.test1.binary'
    TEST_PROC = 'com.example.proc1.binary'
    log = txaio.make_logger()

    def proc1(self, logname, url, loop, counter, payload, details=None):
        fingerprint = hashlib.sha256(payload).digest()[:6]
        self.log.info(
            '{logprefix}: INVOCATION received on pid={pid} from {sender} -> loop={loop}, counter={counter}, len={payload_len}, fp={fp}, caller={caller}, caller_authid={caller_authid}, caller_authrole={caller_authrole}, forward_for={forward_for}',
            logprefix=hl('WAMP {}:{}'.format(self._url, self._logname), color='blue', bold=True),
            pid=hl(self._pid, color='blue', bold=True),
            sender=hl('{}:{}'.format(url, logname), color='blue', bold=True),
            loop=loop,
            counter=counter,
            procedure=details.procedure,
            payload_len=len(payload),
            fp=hl(binascii.b2a_hex(fingerprint).decode(), color='blue', bold=True),
            caller=hl(details.caller, color='blue', bold=True),
            caller_authid=hl(details.caller_authid, color='blue', bold=True),
            caller_authrole=hl(details.caller_authrole, color='blue', bold=True),
            forward_for=details.forward_for)

        fingerprint = hashlib.sha256(payload).digest()[:6]

        self._received_calls_cnt += 1
        self._received_calls_bytes += len(payload)
        if details.forward_for:
            self._received_calls_ff_cnt += 1

        return fingerprint, self._pid, self._logname, self._url

    def on_event1(self, logname, url, loop, counter, payload, details=None):
        fingerprint = hashlib.sha256(payload).digest()[:6]
        self.log.debug('{logprefix}: EVENT received from {sender} -> loop={loop}, counter={counter}, len={payload_len}, fp={fp}, publisher={publisher}, publisher_authid={publisher_authid}, publisher_authole={publisher_authrole}, forward_for={forward_for}',
                       logprefix=hl('WAMP {}:{}'.format(self._url, self._logname), color='blue', bold=True),
                       sender=hl('{}:{}'.format(url, logname), color='blue', bold=True),
                       loop=loop,
                       counter=counter,
                       topic=details.topic,
                       payload_len=len(payload),
                       fp=hl(binascii.b2a_hex(fingerprint).decode(), color='blue', bold=True),
                       publisher=hl(details.publisher, color='blue', bold=True),
                       publisher_authid=hl(details.publisher_authid, color='blue', bold=True),
                       publisher_authrole=hl(details.publisher_authrole, color='blue', bold=True),
                       forward_for=details.forward_for)
        self._received_cnt += 1
        self._received_bytes += len(payload)
        if details.forward_for:
            self._received_ff_cnt += 1

    @inlineCallbacks
    def onJoin(self, details):
        self._pid = os.getpid()

        # benchmark parametrization:
        self._period = self.config.extra.get('period', 10)
        self._loops = self.config.extra.get('loops', 1)
        self._rate = self.config.extra.get('rate', 1)
        self._stride = self.config.extra.get('stride', 1)
        self._size = self.config.extra.get('size', 256)
        self._logname = self.config.extra.get('logname', None)
        self._url = self.config.extra.get('url', None)
        self._silent = self.config.extra.get('silent', False)

        self._batch_id = uuid.uuid4()
        self._running = True
        self._pinfo = ProcessInfo()

        # run-time session statistics for EVENTs
        self._received_cnt = 0
        self._received_bytes = 0
        self._received_ff_cnt = 0
        self._published_cnt = 0
        self._published_bytes = 0

        # run-time session statistics for CALLs
        self._received_calls_cnt = 0
        self._received_calls_bytes = 0
        self._received_calls_ff_cnt = 0
        self._calls_cnt = 0
        self._calls_bytes = 0

        self.log.info('{logname} connected [batch="{batch_id}"]: {details}',
                      logname=self._logname, batch_id=hl(self._batch_id), details=details)

        self._last_stats = None
        self._stats_loop = None

        if self._silent:
            self._stats(self._batch_id, self.log.info)

        stats_period = 10.
        if stats_period:
            self._stats_loop = LoopingCall(self._stats, self._batch_id, self.log.info)
            self._stats_loop.start(stats_period)

        yield self.subscribe(self.on_event1,
                             HATestClientSession.TEST_TOPIC,
                             options=SubscribeOptions(match='exact', details=True))

        for i in range(self._loops):
            self._sender_loop('{}.{}'.format(self._logname, i))

        self.log.info('{logname} ready [period={period}, loops={loops}, rate={rate}, stride={stride}, size={size}]',
                      logname=self._logname, period=self._period, loops=self._loops, rate=self._rate,
                      stride=self._stride, size=self._size)

    def onLeave(self, details):
        self.log.info('{logname} leaving: reason="{reason}"', logname=self._logname, reason=details.reason)
        self._running = False

        if self._silent:
            self._stats(self._batch_id, self.log.warn)

        if self._stats_loop:
            self._stats_loop.stop()
            self._stats_loop = None

    @inlineCallbacks
    def _sender_loop(self, loopname, enable_publish=True, enable_call=True):
        loop = 0
        while self._running:
            started = time_ns()
            dl = []
            for counter in range(self._stride):
                payload = os.urandom(self._size)
                fingerprint = hashlib.sha256(payload).digest()[:6]

                if enable_publish:
                    d = self.publish(HATestClientSession.TEST_TOPIC,
                                     self._logname,
                                     self._url,
                                     loop,
                                     counter,
                                     payload,
                                     options=PublishOptions(acknowledge=True, exclude_me=False))
                    dl.append(d)
                    self._published_cnt += 1
                    self._published_bytes += len(payload)

                    self.log.debug(
                        '{logprefix}: EVENT sent from session={session}, authid={authid}, authrole={authrole} -> loop={loop}, counter={counter}, len={payload_len}, fp={fp}',
                        logprefix=hl('WAMP {}:{}'.format(self._url, self._logname), color='green', bold=True),
                        session=hl(self._session_id, color='green', bold=True),
                        authid=hl(self._authid, color='green', bold=True),
                        authrole=hl(self._authrole, color='green', bold=True),
                        loop=loop,
                        counter=counter,
                        topic=HATestClientSession.TEST_TOPIC,
                        payload_len=len(payload),
                        fp=hl(binascii.b2a_hex(fingerprint).decode(), color='green', bold=True))

                if enable_call:
                    for uri in ['node{}.container1.proc1'.format(i + 1) for i in range(4)]:
                        d = self.call(uri,
                                      self._logname,
                                      self._url,
                                      loop,
                                      counter,
                                      payload,
                                      options=CallOptions(details=True))

                        def check_result(result, uri):
                            print('-' * 100, result)
                            _fingerprint, _pid, _logname, _url = result.results[0]
                            self.log.info('{logprefix}: CALL RESULT for {uri} received from pid={pid}, logname={logname}, url={url}, callee={callee}, callee_authid={callee_authid}, callee_authrole={callee_authrole}, forward_for={forward_for}, fp={fp} => fp_equal={fp_equal}',
                                          logprefix=hl('WAMP {}:{}'.format(self._url, self._logname), color='green',
                                                       bold=True),
                                          pid=hl(_pid, color='green', bold=True),
                                          logname=_logname,
                                          url=_url,
                                          fp=hl(binascii.b2a_hex(fingerprint).decode(), color='green', bold=True),
                                          fp_equal=(_fingerprint == fingerprint),
                                          uri=hl(uri, color='yellow', bold=True),
                                          callee=result.callee,
                                          callee_authid=result.callee_authid,
                                          callee_authrole=result.callee_authrole,
                                          forward_for=result.forward_for)
                            assert _fingerprint == fingerprint

                        def error(err):
                            print(err)

                        d.addCallbacks(check_result, error, (uri,))

                        dl.append(d)
                        self._calls_cnt += 1
                        self._calls_bytes += len(payload)

                        self.log.info(
                            '{logprefix}: CALL issued to {uri} from pid={pid}, session={session}, authid={authid}, authrole={authrole} -> loop={loop}, counter={counter}, len={payload_len}, fp={fp}',
                            logprefix=hl('WAMP {}:{}'.format(self._url, self._logname), color='green', bold=True),
                            pid=hl(self._pid, color='green', bold=True),
                            session=hl(self._session_id, color='green', bold=True),
                            authid=hl(self._authid, color='green', bold=True),
                            authrole=hl(self._authrole, color='green', bold=True),
                            uri=hl(uri, color='yellow', bold=True),
                            loop=loop,
                            counter=counter,
                            procedure=HATestClientSession.TEST_PROC,
                            payload_len=len(payload),
                            fp=hl(binascii.b2a_hex(fingerprint).decode(), color='green', bold=True))

            d = gatherResults(dl)
            try:
                yield d
            except TransportLost:
                self.log.error('Transport lost!')
                self.leave()
                return
            duration = (time_ns() - started) / 10**9
            sleep_secs = (1 / float(self._rate)) - duration
            if sleep_secs > 0:
                yield sleep(sleep_secs)

            loop += 1

    def _stats(self, batch_id, log):

        stats = self._pinfo.get_stats()

        if self._last_stats:
            batch_duration = (stats['time'] - self._last_stats['time']) / 10 ** 9
            ctx = round((stats['voluntary'] - self._last_stats['voluntary']) / batch_duration, 0)

            log('{logprefix}: {user} user, {system} system, {mem_percent} mem_percent, {ctx} ctx',
                logprefix=hl('LOAD', color='white', bold=True),
                user=stats['user'],
                system=stats['system'],
                mem_percent=round(stats['mem_percent'], 1),
                ctx=ctx)

            events_received_per_sec = int(round(self._received_cnt / batch_duration))
            bytes_received_per_sec = int(round(self._received_bytes / batch_duration))
            events_published_per_sec = int(round(self._published_cnt / batch_duration))
            bytes_published_per_sec = int(round(self._published_bytes / batch_duration))

            log('{logprefix}: {events_received} EVENTs received ({events_received_ff} forwarded), {events_received_per_sec}, {events_published} events published, {events_published_per_sec} events/second',
                logprefix=hl('WAMP {}.*'.format(self._logname), color='white', bold=True),
                events_received=self._received_cnt,
                events_received_ff=self._received_ff_cnt,
                events_received_per_sec=hl('{} events/second'.format(events_received_per_sec), color='white', bold=True),
                bytes_received_per_sec=bytes_received_per_sec,
                events_published=self._published_cnt,
                events_published_per_sec=events_published_per_sec,
                bytes_published_per_sec=bytes_published_per_sec)

            calls_received_per_sec = int(round(self._received_calls_cnt / batch_duration))
            call_bytes_received_per_sec = int(round(self._received_calls_bytes / batch_duration))
            calls_issued_per_sec = int(round(self._calls_cnt / batch_duration))
            call_bytes_issued_per_sec = int(round(self._calls_bytes / batch_duration))

            log('{logprefix}: {calls_received} INVOCATIONs received ({calls_received_ff} forwarded), {calls_received_per_sec}, {calls_issued} calls issued, {calls_issued_per_sec} calls/second',
                logprefix=hl('WAMP {}.*'.format(self._logname), color='white', bold=True),
                calls_received=self._received_calls_cnt,
                calls_received_ff=self._received_calls_ff_cnt,
                calls_received_per_sec=hl('{} calls/second'.format(calls_received_per_sec), color='white', bold=True),
                call_bytes_received_per_sec=call_bytes_received_per_sec,
                calls_issued=self._calls_cnt,
                calls_issued_per_sec=calls_issued_per_sec,
                call_bytes_issued_per_sec=call_bytes_issued_per_sec)

            self._received_cnt = 0
            self._received_bytes = 0
            self._received_ff_cnt = 0
            self._published_cnt = 0
            self._published_bytes = 0

            self._received_calls_cnt = 0
            self._received_calls_bytes = 0
            self._received_calls_ff_cnt = 0
            self._calls_cnt = 0
            self._calls_bytes = 0

        self._last_stats = stats


class HATestClient(object):
    def __init__(self, reactor, urls, realm, extra):
        self._reactor = reactor
        self._urls = urls
        self._realm = realm
        self._extra = extra
        self._runners = {}

    def start(self):
        dl = []
        for url in self._urls:
            extra = copy.deepcopy(self._extra)
            extra['url'] = url
            runner = ApplicationRunner(url=url, realm=self._realm, extra=extra)
            self._runners[url] = runner
            d = runner.run(HATestClientSession, auto_reconnect=True, start_reactor=False, reactor=self._reactor)
            dl.append(d)
        return gatherResults(dl)

    def stop(self):
        dl = []
        for runner in self._runners.values():
            d = runner.stop()
            dl.append(d)
        return gatherResults(dl)


@inlineCallbacks
def main(reactor, config, logname, url, realm, connections, loops, rate, stride, size, period, duration, silent):

    if url:
        urls = [url]
    else:
        urls = []
        for node in config.sections():
            url = config[node].get('url', None)
            if url:
                urls.append(url)

    pprint(urls)

    extra = {
        'period': period,
        'loops': loops,
        'rate': rate,
        'stride': stride,
        'size': size,
        'silent': silent,
    }
    clients = []

    dl = []
    for i in range(connections):
        _extra = copy.deepcopy(extra)
        _extra['logname'] = '{}.{}'.format(logname, i)

        client = HATestClient(reactor, urls, realm, _extra)
        clients.append(client)

        d = client.start()
        dl.append(d)

    yield gatherResults(dl)

    yield sleep(duration)

    dl = []
    for client in clients:
        d = client.stop()
        dl.append(d)

    yield gatherResults(dl)


if __name__ == '__main__':

    print('Client with PID {} starting ..'.format(hl(os.getpid(), bold=True)))

    parser = argparse.ArgumentParser()

    parser.add_argument('-d',
                        '--debug',
                        action='store_true',
                        help='Enable debug output (set log level "debug").')

    parser.add_argument('--config',
                        dest='config',
                        type=str,
                        default='client.ini',
                        help='Client WAMP router connections configuration.')

    parser.add_argument('-s',
                        '--silent',
                        action='store_true',
                        help='Silent mode (set log level "warn").')

    parser.add_argument('--logname',
                        dest='logname',
                        type=str,
                        default='client0',
                        help='Log name to use (default: "publisher0").')

    parser.add_argument('--url',
                        dest='url',
                        type=str,
                        default=None,
                        help='The proxied router URL or None for connecting directly to nodes.')

    parser.add_argument('--realm',
                        dest='realm',
                        type=str,
                        default="realm1",
                        help='The realm to join (default: "realm1").')

    parser.add_argument('--connections',
                        dest='connections',
                        type=int,
                        default=1,
                        help='Number of connections to open (default: 1).')

    parser.add_argument('--duration',
                        dest='duration',
                        type=int,
                        default=60,
                        help='Test duration in seconds (default: 60).')

    parser.add_argument('--period',
                        dest='period',
                        type=int,
                        default=10,
                        help='Publishing session logging period in seconds (default: 10).')

    parser.add_argument('--loops',
                        dest='loops',
                        type=int,
                        default=1,
                        help='Number of publishing loops per connections to run (default: 1).')

    parser.add_argument('--rate',
                        dest='rate',
                        type=float,
                        default=1.,
                        help='Publishing (nominal) loop rate in Hz (default: 1).')

    parser.add_argument('--stride',
                        dest='stride',
                        type=int,
                        default=1,
                        help='Number of events to publish per loop iteration (default: 1).')

    parser.add_argument('--size',
                        dest='size',
                        type=int,
                        default=256,
                        help='Event application payload size in bytes (default: 256).')

    args = parser.parse_args()

    if args.silent:
        txaio.start_logging(level='warn')
    elif args.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    log = txaio.make_logger()

    config = configparser.ConfigParser()
    with open(args.config) as f:
        config.read_file(f)

    sys.exit(react(main, (config,
                          args.logname,
                          args.url,
                          args.realm,
                          args.connections,
                          args.loops,
                          args.rate,
                          args.stride,
                          args.size,
                          args.period,
                          args.duration,
                          args.silent)))
