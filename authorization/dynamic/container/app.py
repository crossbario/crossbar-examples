from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks

class App(ApplicationSession):

    def onConnect(self):
        self.join(self.config.realm, [u'ticket'], u'app')

    def onChallenge(self, challenge):
        if challenge.method == u'ticket':
            return u'secret456'
        else:
            raise Exception('Invalid authmethod {}'.format(challenge.method))

    @inlineCallbacks
    def onJoin(self, details):
        yield self.register(self.test, u'com.example.test')
        self.log.info('procedure successfully registered!')

    def test(self):
        pass
