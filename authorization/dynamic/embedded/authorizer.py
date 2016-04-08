from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks

class Authorizer(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        yield self.register(self.authorize, u'com.example.auth')

    def authorize(self, session, uri, action):
        self.log.info('authorize: session={session}, uri={uri}, action={action}', session=session, uri=uri, action=action)
        return True
