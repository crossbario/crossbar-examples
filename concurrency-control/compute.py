import os
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


def fib(n):
    if n == 1 or n == 2:
        return 1
    return fib(n - 1) + fib(n - 2)


def do_compute(call_no, mode='sleep', runtime=None, n=None):
    started = utcnow()
    process_id = os.getpid()
    thread_id = _thread.get_ident()

    if mode == 'fib':
        res = fib(n)
    elif mode == 'sleep':
        # yes, we do the evil blocking thing here!
        # this is to simulate CPU intensive stuff
        time.sleep(runtime)
        res = None
    else:
        res = random.random()

    ended = utcnow()

    result = {
        u'call_no': call_no,
        u'started': started,
        u'ended': ended,
        u'process': process_id,
        u'thread': thread_id,
        u'result': res
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
    def compute(self, call_no, mode='sleep', runtime=None, n=None):
        self._invocations_served += 1
        self._current_concurrency += 1
        self.log.info('starting compute() on background thread (current concurrency {current_concurrency} of max {max_concurrency}) ..', current_concurrency=self._current_concurrency, max_concurrency=self._max_concurrency)

        # now run our compute kernel on a background thread from the default Twisted reactor thread pool ..
        res = yield deferToThread(do_compute, call_no, mode, runtime, n)

        self._current_concurrency -= 1
        self.log.info('compute() ended from background thread ({invocations} invocations, current concurrency {current_concurrency} of max {max_concurrency})', invocations=self._invocations_served, current_concurrency=self._current_concurrency, max_concurrency=self._max_concurrency)
        returnValue(res)
