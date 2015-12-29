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


class MyAuthenticator(ApplicationSession):

   # our "database" of accepted client certificate fingerprints
   ACCEPTED_CERTS = set([u'B6:E5:E6:F2:2A:86:DB:3C:DC:9F:51:42:58:39:9B:14:92:5D:A1:EB'])

   @inlineCallbacks
   def onJoin(self, details):

      def authenticate(realm, authid, details):
         # This is a trivial dynamic authenticator that checks if the TLS client
         # certificate presented by the connecting client has a fingerprint that
         # is contained in ACCEPTED_CERTS.
         # If so, it accepts the client, setting the fixed authrole='backend' and
         # setting the authid to the certificate subject common name (and hence, the
         # authid provided by the WAMP client becomes irrelevant).

         if 'client_cert' not in details['transport'] or not details['transport']['client_cert']:
            raise ApplicationError(u"com.example.no_cert", u"no client certificate presented")

         client_cert = details['transport']['client_cert']
         sha1 = client_cert['sha1']

         subject_cn = client_cert['subject']['cn']
         issuer_cn = client_cert['issuer']['cn']

         print("MyAuthenticator.authenticate: realm='{}', authid='{}', subject_cn='{}', issuer_cn='{}', sha1={}".format(realm, authid, subject_cn, issuer_cn, sha1))

         if sha1 not in self.ACCEPTED_CERTS:
            print("MyAuthenticator.authenticate: client denied.")
            raise ApplicationError(u"com.example.invalid_cert", u"certificate with SHA1 {} denied".format(sha1))
         else:
            print("MyAuthenticator.authenticate: client accepted.")
            return {
               # here, we are returning the client certificate subject CN, but
               # we could also use the certificate fingerprint as authid or remap
               # the fingerprint to yet some other authid
               u'authid': subject_cn,

               # here, we set the authrole to a fixed value "backend". we could also
               # do a database lookup here, or parse the client cert CN is both an
               # authid and authrole (eg consider CN="node301#backend")
               u'role': u'backend'
            }

      # register our dynamic authenticator so Crossbar.io is aware of and can call it
      #
      try:
         yield self.register(authenticate, 'com.example.authenticate')
         print("MyAuthenticator: dynamic authenticator registered.")
      except Exception as e:
         print("MyAuthenticator: could not register dynamic authenticator - {}".format(e))
