import os
from pprint import pprint


from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError

MYTICKET = os.environ.get('MYTICKET', None)

# our principal "database"
PRINCIPALS_DB = {
   "joe": {
      "ticket": "secret!!!",
      "role": "frontend"
   },
   "client2": {
      "ticket": "123sekret",
      "role": "frontend"
   },
   "client1": {
      "ticket": MYTICKET,
      "role": "frontend"
   }
}


class AuthenticatorSession(ApplicationSession):

   @inlineCallbacks
   def onJoin(self, details):

      def authenticate(realm, authid, details):
         ticket = details['ticket']
         print("WAMP-Ticket dynamic authenticator invoked: realm='{}', authid='{}', ticket='{}'".format(realm, authid, ticket))
         pprint(details)

         if authid in PRINCIPALS_DB:
            if ticket == PRINCIPALS_DB[authid]['ticket']:
               return PRINCIPALS_DB[authid]['role']
            else:
               raise ApplicationError("com.example.invalid_ticket", "could not authenticate session - invalid ticket '{}' for principal {}".format(ticket, authid))
         else:
            raise ApplicationError("com.example.no_such_user", "could not authenticate session - no such principal {}".format(authid))

      try:
         yield self.register(authenticate, 'com.example.authenticate')
         print("WAMP-Ticket dynamic authenticator registered!")
      except Exception as e:
         print("Failed to register dynamic authenticator: {0}".format(e))
