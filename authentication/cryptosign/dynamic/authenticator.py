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

import six

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError


# a simple principals database. in real world use, this likey would be
# replaced by some persistent database used to store principals.
PRINCIPALS = [
   {
      # when a session is authenticating use one of the authorized_keys,
      # then assign it all the data below
      u"authid": u"client01@example.com",
      u"realm": u"devices",
      u"role": u"device",
      u"extra": {
         "foo": 23
      },
      u"authorized_keys": [
         u"545efb0a2192db8d43f118e9bf9aee081466e1ef36c708b96ee6f62dddad9122"
      ]
   },
   {
      u"authid": u"client02@example.com",
      u"realm": u"devices",
      u"role": u"device",
      u"extra": {
         "foo": 42,
         "bar": "baz"
      },
      u"authorized_keys": [
         u"9c194391af3bf566fc11a619e8df200ba02efb35b91bdd98b424f20f4163875e",
         u"585df51991780ee8dce4766324058a04ecae429dffd786ee80839c9467468c28"
      ]
   }
]


class AuthenticatorSession(ApplicationSession):

   @inlineCallbacks
   def onJoin(self, details):

      # build a map from pubkeys to principals
      pubkey_to_principals = {}
      for p in PRINCIPALS:
         for k in p[u'authorized_keys']:
            if k in pubkey_to_principals:
               raise Exception("ambiguous key {}".format(k))
            else:
               pubkey_to_principals[k] = p

      # this is our dynamic authenticator procedure that will be called by Crossbar.io
      # when a session is authenticating
      def authenticate(realm, authid, details):
         self.log.debug("authenticate({realm}, {authid}, {details})", realm=realm, authid=authid, details=details)

         assert(u'authmethod' in details)
         assert(details[u'authmethod'] == u'cryptosign')
         assert(u'authextra' in details)
         assert(u'pubkey' in details[u'authextra'])

         pubkey = details[u'authextra'][u'pubkey']
         self.log.info("authenticating session with public key = {pubkey}", pubkey=pubkey)

         if pubkey in pubkey_to_principals:
            principal = pubkey_to_principals[pubkey]
            auth = {
               u'pubkey': pubkey,
               u'realm': principal[u'realm'],
               u'authid': principal[u'authid'],
               u'role': principal[u'role'],
               u'extra': principal[u'extra'],
               u'cache': True
            }
            self.log.info("found valid principal {authid} matching public key", authid=auth[u'authid'])
            return auth
         else:
            self.log.error("no principal found matching public key")
            raise ApplicationError('com.example.no_such_user', 'no principal with matching public')

      # register our dynamic authenticator with Crossbar.io
      try:
         yield self.register(authenticate, 'com.example.authenticate')
         self.log.info("Dynamic authenticator registered!")
      except Exception as e:
         self.log.info("Failed to register dynamic authenticator: {0}".format(e))
