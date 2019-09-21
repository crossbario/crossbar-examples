import os
import hashlib
import binascii

import txaio
txaio.use_twisted()

from txaio import make_logger
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.types import RegisterOptions

from crossbar._util import hl


class Backend(ApplicationSession):
    TEST_PROC = 'com.example.proc1.binary'

    log = make_logger()

    def __init__(self, config):
        self.log.info('Backend.__init__()')
        ApplicationSession.__init__(self, config)

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info('Backend.onJoin(details={details})', details=details)

        self._pid = os.getpid()
        self._logname = self.config.extra.get('logname', None)
        self._url = self.config.extra.get('url', None)

        # run-time session statistics for CALLs
        self._received_calls_cnt = 0
        self._received_calls_bytes = 0
        self._received_calls_ff_cnt = 0

        uri = Backend.TEST_PROC
        uri = '{}.proc1'.format(self._logname)

        def proc1(logname, url, loop, counter, payload, details=None):
            fingerprint = hashlib.sha256(payload).digest()[:6]
            self.log.info(
                '{logprefix}: INVOCATION received for {uri} on pid={pid} from {sender} -> loop={loop}, counter={counter}, len={payload_len}, fp={fp}, caller={caller}, caller_authid={caller_authid}, caller_authrole={caller_authrole}, forward_for={forward_for}',
                logprefix=hl('WAMP {}:{}'.format(self._url, self._logname), color='blue', bold=True),
                pid=hl(self._pid, color='blue', bold=True),
                sender=hl('{}:{}'.format(url, logname), color='blue', bold=True),
                loop=loop,
                counter=counter,
                procedure=details.procedure,
                payload_len=len(payload),
                uri=hl(uri, color='yellow', bold=True),
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

        yield self.register(proc1, uri,
                            options=RegisterOptions(match='exact', invoke='random', details_arg='details'))

        self.log.info('Backend procedure registered at {uri}', uri=hl(uri))

