import time
import random

from six.moves import _thread

import txaio
txaio.use_twisted()

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, returnValue

from autobahn.util import utcnow
from autobahn.wamp.types import RegisterOptions
from autobahn.twisted.wamp import ApplicationSession

from twisted.internet.threads import deferToThread


log = txaio.make_logger()

def do_compute(call_no, runtime):
    started = utcnow()
    thread_id = _thread.get_ident()
    #log.info("compute() invoked on thread ID {thread_id}", thread_id=thread_id)

    # yes, we do the evil blocking thing here!
    # this is to simulate CPU intensive stuff
    time.sleep(runtime)

    result = {
        u'call_no': call_no,
        u'started': started,
        u'thread': thread_id,
        u'value': random.random()
    }
    return result


class ComputeKernel(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        self._max_concurrency = self.config.extra[u'concurrency']
        self._current_concurrency = 0
        self._invocations_served = 0

        # adjust the background thread pool size
        reactor.suggestThreadPoolSize(self._max_concurrency)

        yield self.register(self.compute, u'com.example.compute', options=RegisterOptions(invoke=u'roundrobin', concurrency=self._max_concurrency))
        self.log.info('ComputeKernel ready with concurrency {}!'.format(self._max_concurrency))

    @inlineCallbacks
    def compute(self, call_no, runtime=10):
        self._invocations_served += 1
        self._current_concurrency += 1
        self.log.info('starting compute() on background thread (current concurrency {current_concurrency} of max {max_concurrency}) ..', current_concurrency=self._current_concurrency, max_concurrency=self._max_concurrency)

        # now run our compute kernel on a background thread from the default Twisted reactor thread pool ..
        res = yield deferToThread(do_compute, call_no, runtime)

        self._current_concurrency -= 1
        self.log.info('compute() ended from background thread ({invocations} invocations, current concurrency {current_concurrency} of max {max_concurrency})', invocations=self._invocations_served, current_concurrency=self._current_concurrency, max_concurrency=self._max_concurrency)
        returnValue(res)
