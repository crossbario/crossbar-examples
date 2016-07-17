###############################################################################
##
##  Copyright (C) 2015, Tavendo GmbH and/or collaborators. All rights reserved.
##
##  Redistribution and use in source and binary forms, with or without
##  modification, are permitted provided that the following conditions are met:
##
##  1. Redistributions of source code must retain the above copyright notice,
##     this list of conditions and the following disclaimer.
##
##  2. Redistributions in binary form must reproduce the above copyright notice,
##     this list of conditions and the following disclaimer in the documentation
##     and/or other materials provided with the distribution.
##
##  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
##  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
##  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
##  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
##  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
##  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
##  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
##  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
##  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
##  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
##  POSSIBILITY OF SUCH DAMAGE.
##
###############################################################################

import time
import random

from six.moves import _thread

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, returnValue

from autobahn.wamp.types import RegisterOptions
from autobahn.twisted.wamp import ApplicationSession

from twisted.internet.threads import deferToThread


def compute(runtime):
    thread_id = _thread.get_ident()
    print("compute() invoked on thread ID {}".format(thread_id))

    # yes, we do the evil blocking thing here!
    # this is to simulate CPU intensive stuff
    time.sleep(runtime)

    return random.random()


class ComputeKernel(ApplicationSession):

    max_concurrency = 4

    @inlineCallbacks
    def onJoin(self, details):
        self._current_concurrency = 0
        self._invocations = 0

        # adjust the background thread pool size
        reactor.suggestThreadPoolSize(self.max_concurrency)

        yield self.register(self.compute, u'com.example.compute', options=RegisterOptions(concurrency=self.max_concurrency))
        self.log.info('ComputeKernel ready with concurrency {}!'.format(self.max_concurrency))

    @inlineCallbacks
    def compute(self, runtime=10):
        self._invocations += 1
        self._current_concurrency += 1
        self.log.info('starting compute() on background thread ({current_concurrency} current concurrency of max {max_concurrency}) ..', current_concurrency=self._current_concurrency, max_concurrency=self.max_concurrency)

        # now run our compute kernel on a background thread from the default Twisted reactor thread pool ..
        res = yield deferToThread(self._compute, runtime)

        self._current_concurrency -= 1
        self.log.info('compute() ended from background thread ({invocations} invocations, {current_concurrency} current concurrency of max {max_concurrency})', invocations=self._invocations, current_concurrency=self._current_concurrency, max_concurrency=self.max_concurrency)
        returnValue(res)
