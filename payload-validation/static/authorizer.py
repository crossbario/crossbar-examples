from twisted.internet.defer import inlineCallbacks

from autobahn.util import hltype, hlval
from autobahn.twisted.wamp import ApplicationSession


class ExampleAuthorizer(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        yield self.register(self.authorize, 'com.example.authorize')
        self.log.info('{func} ok, ready!', func=hltype(self.onJoin))

    def authorize(self, session, uri, action, _):
        self.log.info('{func}: authrole="{authrole}", uri="{uri}", action="{action}"',
                      func=hltype(self.authorize),
                      authrole=hlval(session['authrole']),
                      uri=hlval(uri),
                      action=hlval(action))

        if (session['authrole'] == 'frontend' and uri.startswith('com.example.backend.') and
                action in ['call', 'subscribe']):
            return {
                'allow': True,
                'cache': False,  # optional
                'disclose': True,  # optional
            }
        else:
            # you can just return True/False here, which is a shortcut
            # for {"allow": True/False}
            return False
