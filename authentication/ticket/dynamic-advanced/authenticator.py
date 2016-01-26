###############################################################################
##
##  Copyright (C) Tavendo GmbH and/or collaborators. All rights reserved.
##
##  Redistribution and use in source and binary forms, with or without
##  modification, are permitted provided that the following conditions are met:
##
##  1. Redistributions of source code must retain the above copyright notice,
##     this list of conditions and the following disclaimer.
##
##  2. Redistributions in binary form must reproduce the above copyright notice,
##     this list of conditions and the following disclaimer in the documentation
##     and/or other materials provided with the distribution.
##
##  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
##  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
##  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
##  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
##  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
##  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
##  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
##  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
##  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
##  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
##  POSSIBILITY OF SUCH DAMAGE.
##
###############################################################################

import os

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError


# our principal "database"
PRINCIPALS_DB = {
   u'user1': {
      u'realm': u'realm-user1',
      u'role': u'user',
      u'ticket': u'123secret'
   },
   u'user2': {
      u'realm': u'realm-user2',
      u'role': u'user',
      u'ticket': u'456secret'
   }
}

from crossbar.common.checkconfig import pprint_json


class AuthenticatorSession(ApplicationSession):

   @inlineCallbacks
   def onJoin(self, details):

      print("WAMP-Ticket dynamic authenticator joined: {}".format(details))

      def authenticate(realm, authid, details):
         print("WAMP-Ticket dynamic authenticator invoked: realm='{}', authid='{}', details=".format(realm, authid))
         pprint_json(details)

         if authid in PRINCIPALS_DB:
            ticket = details['ticket']
            principal = PRINCIPALS_DB[authid]

            if ticket != principal['ticket']:
               raise ApplicationError(u'com.example.invalid_ticket', "could not authenticate session - invalid ticket '{}' for principal {}".format(ticket, authid))

            if realm and realm != principal[u'realm']:
               raise ApplicationError(u'com.example_invalid_realm', "user {} should join {}, not {}".format(authid, principal[u'realm'], realm))

            res = {
               u'realm': principal[u'realm'],
               u'role': principal[u'role'],
               u'extra': {
                  u'my-custom-welcome-data': [1, 2, 3]
               }
            }
            print("WAMP-Ticket authentication success: {}".format(res))
            return res
         else:
            raise ApplicationError("com.example.no_such_user", "could not authenticate session - no such principal {}".format(authid))

      try:
         yield self.register(authenticate, 'com.example.authenticate')
         print("WAMP-Ticket dynamic authenticator registered!")
      except Exception as e:
         print("Failed to register dynamic authenticator: {0}".format(e))
