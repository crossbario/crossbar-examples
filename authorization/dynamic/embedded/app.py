from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks

class App(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        yield self.register(self.test, u'com.example.test')
        self.log.info('procedure successfully registered!')

    def test(self):
        pass
