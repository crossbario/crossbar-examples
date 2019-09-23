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

    log = make_logger()

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

        self.log.info('*' * 80)
        self.log.info('Backend procedure registered at {uri}', uri=hl(uri))
        self.log.info('*' * 80)

