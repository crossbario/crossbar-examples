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
from pprint import pprint

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError
from autobahn.wamp.auth import check_totp

# our principal "database"
PRINCIPALS_DB = {
   u"tobias1": {
      u"seed": u"CACKN3GRF3KQZMEK",
      u"role": u"frontend"
   },
   u"user1": {
      u"seed": u"BKIV3FXPRA67N4Q5",
      u"role": u"frontend"
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
            secret = PRINCIPALS_DB[authid][u'seed']
            if check_totp(secret, ticket):
               return PRINCIPALS_DB[authid][u'role']
            else:
               raise ApplicationError(u'com.example.invalid_ticket', u'could not authenticate session - invalid ticket "{}" for principal {}'.format(ticket, authid))
         else:
            raise ApplicationError(u'com.example.no_such_user', u'could not authenticate session - no such principal {}'.format(authid))

      try:
         yield self.register(authenticate, u'com.example.authenticate')
         print("WAMP-Ticket dynamic authenticator registered!")
      except Exception as e:
         print("Failed to register dynamic authenticator: {0}".format(e))
