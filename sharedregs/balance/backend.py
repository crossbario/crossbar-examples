
import os
import sys

from twisted.python import log
from twisted.internet.defer import inlineCallbacks, returnValue

from autobahn import wamp
from autobahn.wamp.types import RegisterOptions
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner
from autobahn.twisted.util import sleep


class MyComponent(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        self._ident = "MyComponent (PID {}, Session {})".format(os.getpid(), details.session)
        self.call_count = 0
        yield self.register(self.add2, u'com.example.add2', options=RegisterOptions(invoke=u'balance'))
        log.msg("MyComponent: add2() registered!")

    @inlineCallbacks
    def add2(self, a, b, busy=0.1):
        self.call_count += 1
        log.msg("{}: add2 called on {} with effort {}".format(self.call_count, self._ident, busy))
        yield sleep(busy)
        # print("--{}--".format(self.call_count))
        returnValue({'result': a + b, 'ident': self._ident, 'callnum': self.call_count})


if __name__ == '__main__':
    log.startLogging(sys.stdout)
    runner = ApplicationRunner(url=u"ws://127.0.0.1:8080/ws", realm=u"realm1")
    runner.run(MyComponent)

