from pprint import pprint

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError


# our user "database"
USERDB = {
   'client1': {
      # these are required:
      'secret': 'secret123',  # the secret/password to be used
      'role': 'frontend'    # the auth role to be assigned when authentication succeeds
   },
   'joe': {
      # these are required:
      'secret': 'secret2',  # the secret/password to be used
      'role': 'frontend'    # the auth role to be assigned when authentication succeeds
   },
   'hans': {
      'authid': 'ID09125',  # assign a different auth ID during authentication
      'secret': '123456',
      'role': 'frontend'
   },
   'peter': {
      # use salted passwords

      # autobahn.wamp.auth.derive_key(secret.encode('utf8'), salt.encode('utf8')).decode('ascii')
      'secret': 'prq7+YkJ1/KlW1X0YczMHw==',
      'role': 'frontend',
      'salt': 'salt123',
      'iterations': 100,
      'keylen': 16
   }
}


class AuthenticatorSession(ApplicationSession):

   @inlineCallbacks
   def onJoin(self, details):

      def authenticate(realm, authid, details):
         print("WAMP-CRA dynamic authenticator invoked: realm='{}', authid='{}'".format(realm, authid))
         pprint(details)

         if authid in USERDB:
            # return a dictionary with authentication information ...
            return USERDB[authid]
         else:
            raise ApplicationError('com.example.no_such_user', 'could not authenticate session - no such user {}'.format(authid))

      try:
         yield self.register(authenticate, 'com.example.authenticate')
         print("WAMP-CRA dynamic authenticator registered!")
      except Exception as e:
         print("Failed to register dynamic authenticator: {0}".format(e))
