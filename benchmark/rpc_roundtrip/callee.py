from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession


class AppSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        prefix = self.config.extra[u'prefix']
        logname = self.config.extra[u'logname']

        def echo(arg):
            return arg

        yield self.register(echo, u'{}.echo'.format(prefix))
        self.log.info("Ready!")
