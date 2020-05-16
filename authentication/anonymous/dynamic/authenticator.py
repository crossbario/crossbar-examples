from pprint import pprint
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession


class AuthenticatorSession(ApplicationSession):

   @inlineCallbacks
   def onJoin(self, details):

      def authenticate(realm, authid, details):
         print('WAMP-Anonymous dynamic authenticator invoked (realm="{}", authid="{}"'.format(realm, authid))
         pprint(details)
         principal = {
            'role': 'public',
            'extra': {
               'eins': 'zwo',
               'drei': [4, 5, 6]
            }
         }
         pprint(principal)
         return principal

      try:
         yield self.register(authenticate, 'com.example.authenticate')
         print("WAMP-Anonymous dynamic authenticator registered!")
      except Exception as e:
         print("Failed to register dynamic authenticator: {0}".format(e))
