from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks

class App(ApplicationSession):

    def onConnect(self):
        self.join(self.config.realm, ['ticket'], 'app')

    def onChallenge(self, challenge):
        if challenge.method == 'ticket':
            return 'secret456'
        else:
            raise Exception('Invalid authmethod {}'.format(challenge.method))

    @inlineCallbacks
    def onJoin(self, details):
        yield self.register(self.test, 'com.example.test')
        self.log.info('procedure successfully registered!')

    def test(self):
        pass
