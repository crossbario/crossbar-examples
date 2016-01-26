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

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError


# our user "database"
USERDB = {
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

from crossbar.common.checkconfig import pprint_json


class AuthenticatorSession(ApplicationSession):

   @inlineCallbacks
   def onJoin(self, details):

      def authenticate(realm, authid, details):
         print("WAMP-CRA dynamic authenticator invoked: realm='{}', authid='{}'".format(realm, authid))
         pprint_json(details)

         if authid in USERDB:
            # return a dictionary with authentication information ...
            return USERDB[authid]
         else:
            raise ApplicationError(u'com.example.no_such_user', 'could not authenticate session - no such user {}'.format(authid))

      try:
         yield self.register(authenticate, u'com.example.authenticate')
         print("WAMP-CRA dynamic authenticator registered!")
      except Exception as e:
         print("Failed to register dynamic authenticator: {0}".format(e))
