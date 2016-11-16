from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession

class Backend(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        def add2(x, y):
            self.log.info("add2() called with {x} and {y}", x=x, y=y)
            return x + y

        reg = yield self.register(add2, u'com.example.add2')
        self.log.info("procedure add2() registered")
