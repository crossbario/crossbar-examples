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
import os
from os import environ
import argparse
import random

import colorama
from colorama import Fore

from twisted.internet.protocol import ProcessProtocol
from twisted.internet.defer import inlineCallbacks, Deferred, returnValue, gatherResults
from twisted.internet.error import ProcessExitedAlready
from twisted.internet.task import react

from autobahn.twisted.util import sleep
from crossbar._util import hl


class ClientProcessProtocol(ProcessProtocol):

    def __init__(self, all_done, launched, color=None, prefix=''):
        """
        :param all_done: Deferred that gets callback() when our process exits (.errback if it exits non-zero)
        :param launched: Deferred that gets callback() when our process starts.
        """
        self.all_done = all_done
        self.launched = launched
        self.color = color or ''
        self.prefix = prefix
        self._out = ''
        self._err = ''

    def connectionMade(self):
        if not self.launched.called:
            self.launched.callback(self)

    def outReceived(self, data):
        self._out += data.decode('utf8')
        while '\n' in self._out:
            idx = self._out.find('\n')
            line = self._out[:idx]
            self._out = self._out[idx + 1:]
            sys.stdout.write(self.prefix + self.color + line + Fore.RESET + '\n')

    def errReceived(self, data):
        self._err += data.decode('utf8')
        while '\n' in self._err:
            idx = self._err.find('\n')
            line = self._err[:idx]
            self._err = self._err[idx + 1:]
            sys.stderr.write(self.prefix + self.color + line + Fore.RESET + '\n')

    def processEnded(self, reason):
        # reason.value should always be a ProcessTerminated instance
        fail = reason.value
        # print('processEnded', fail)

        if fail.exitCode != 0 and fail.exitCode is not None:
            msg = 'Process exited with code "{}".'.format(fail.exitCode)
            err = RuntimeError(msg)
            self.all_done.errback(err)
            if not self.launched.called:
                self.launched.errback(err)
        else:
            self.all_done.callback(fail)
            if not self.launched.called:
                print("FIXME: _launched should have been callbacked by now.")
                self.launched.callback(self)


@inlineCallbacks
def start_client(reactor, cmd_args, index, py_fname='client.py', color=Fore.YELLOW, prefix='', exe=sys.executable):
    finished = Deferred()
    launched = Deferred()
    protocol = ClientProcessProtocol(finished, launched, color, prefix)

    args = [exe, py_fname]

    if cmd_args.debug:
        args.extend(['--debug'])

    if cmd_args.config:
        args.extend(['--config', cmd_args.config])

    if cmd_args.silent:
        args.extend(['--silent'])

    if cmd_args.url:
        args.extend(['--url', cmd_args.url])

    if cmd_args.realm:
        args.extend(['--realm', cmd_args.realm])

    if cmd_args.connections:
        args.extend(['--connections', str(cmd_args.connections)])

    if cmd_args.loops:
        args.extend(['--loops', str(cmd_args.loops)])

    if cmd_args.rate:
        args.extend(['--rate', str(cmd_args.rate)])

    if cmd_args.stride:
        args.extend(['--stride', str(cmd_args.stride)])

    if cmd_args.size:
        args.extend(['--size', str(cmd_args.size)])

    if cmd_args.period:
        args.extend(['--period', str(cmd_args.period)])

    if cmd_args.duration:
        args.extend(['--duration', str(cmd_args.duration)])

    if cmd_args.logname:
        args.extend(['--logname', cmd_args.logname.format(index)])

    env = environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    reactor.spawnProcess(protocol, exe, args, path='.', env=env)

    yield launched
    returnValue(protocol)


@inlineCallbacks
def main(reactor, args):
    colorama.init()

    pl = []
    for i in range(args.clients):
        proto = yield start_client(reactor, args, i)
        pl.append(proto)

        delay = random.expovariate(1)
        yield sleep(delay)

    pids = [p.transport.pid for p in pl]
    print('Started clients with PIDs {}'.format(hl(pids, bold=True)))

    def shutdown():
        for p in pl:
            try:
                pid = p.transport.pid
                p.transport.signalProcess('KILL')
                print('Client with PID {} killed'.format(hl(pid, bold=True)))
            except ProcessExitedAlready:
                pass

    reactor.addSystemEventTrigger('before', 'shutdown', shutdown)

    success = False
    dl = [p.all_done for p in pl]
    try:
        yield gatherResults(dl)
        success = True
    except Exception as e:
        print("FAILED:", e)

    if success:
        returnValue(0)
    else:
        returnValue(1)


if __name__ == '__main__':

    print('Client with PID {} starting ..'.format(hl(os.getpid(), bold=True)))

    url = os.environ.get('CBURL', u'ws://localhost:8080/ws')
    realm = os.environ.get('CBREALM', u'realm1')

    parser = argparse.ArgumentParser()

    parser.add_argument('-d',
                        '--debug',
                        action='store_true',
                        help='Enable debug output.')

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
                        default='client{}',
                        help='Log name pattern to use (default: "client{}").')

    parser.add_argument('--clients',
                        dest='clients',
                        type=int,
                        default=1,
                        help='Number of clients to spawn (default: 1).')

    parser.add_argument('--url',
                        dest='url',
                        type=str,
                        default=url,
                        help='The router URL (default: "ws://localhost:8080/ws").')

    parser.add_argument('--realm',
                        dest='realm',
                        type=str,
                        default=realm,
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

    sys.exit(react(main, (args,)))
