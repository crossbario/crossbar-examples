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

from twisted.internet import reactor
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp import cryptosign


class ClientSession(ApplicationSession):

   def __init__(self, config=None):
      print("__init__(config={})".format(config))
      ApplicationSession.__init__(self, config)

      # load the client private key (raw format)
      self._key = cryptosign.Key.from_raw(config.extra[u'key'])
      print("Client public key loaded: {}".format(self._key.public_key()))

   def onConnect(self):
      print("onConnect()")

      # authentication extra information for wamp-cryptosign
      #
      extra = {
         # forward the client pubkey: this allows us to omit authid as
         # the router can identify us with the pubkey already
         u'pubkey': self._key.public_key(),

         # not yet implemented. a public key the router should provide
         # a trustchain for it's public key. the trustroot can eg be
         # hard-coded in the client, or come from a command line option.
         u'trustroot': None,

         # not yet implemented. for authenticating the router, this
         # challenge will need to be signed by the router and send back
         # in AUTHENTICATE for client to verify. A string with a hex
         # encoded 32 bytes random value.
         u'challenge': None
      }

      # now request to join ..
      self.join(self.config.realm,
                authmethods=[u'cryptosign'],
                authid=self.config.extra[u'authid'],
                authextra=extra)

   def onChallenge(self, challenge):
      print("onChallenge(challenge={})".format(challenge))
      # alright, we've got a challenge from the router.

      # not yet implemented. check the trustchain the router provided against
      # our trustroot, and check the signature provided by the
      # router for our previous challenge. if both are ok, everything
      # is fine - the router is authentic wrt our trustroot.

      # sign the challenge with our private key.
      signed_challenge = self._key.sign_challenge(challenge)

      # send back the signed challenge for verification
      return signed_challenge

   def onJoin(self, details):
      print("onJoin(details={})".format(details))
      print("""
            Hooray! We've been successfully authenticated
            with WAMP-cryptosign using Ed25519!
            """)
      self.leave()

   def onLeave(self, details):
      print("onLeave(details={})".format(details))
      self.disconnect()

   def onDisconnect(self):
      print("onDisconnect()")
      reactor.stop()


if __name__ == '__main__':

   import sys
   import argparse
   from autobahn.twisted.wamp import ApplicationRunner

   # parse command line arguments
   parser = argparse.ArgumentParser()
   parser.add_argument('--authid', dest='authid', type=unicode, default=None, help='The authid to connect under. If not provided, let the router auto-choose the authid.')
   parser.add_argument('--realm', dest='realm', type=unicode, default=None, help='The realm to join. If not provided, let the router auto-choose the realm.')
   parser.add_argument('--key', dest='key', type=unicode, required=True, help='The private client key to use for authentication. A 32 bytes file containing the raw Ed25519 private key.')
   parser.add_argument('--routerkey', dest='routerkey', type=unicode, default=None, help='The public router key to verify the remote router against. A 32 bytes file containing the raw Ed25519 public key.')
   parser.add_argument('--url', dest='url', type=unicode, default=u'ws://localhost:8080/ws', help='The router URL (default: ws://localhost:8080/ws).')
   parser.add_argument('--agent', dest='agent', type=unicode, default=None, help='Path to Unix domain socket of SSH agent to use.')
   parser.add_argument('--trace', dest='trace', action='store_true', default=False, help='Trace traffic: log WAMP messages sent and received')
   options = parser.parse_args()

   # forward requested authid and key filename to ClientSession
   extra = {
      u'authid': options.authid,
      u'key': options.key
   }
   print("Connecting to {}: realm={}, authid={}".format(options.url, options.realm, options.authid))

   # connect to router and run ClientSession
   runner = ApplicationRunner(url=options.url, realm=options.realm, extra=extra, debug_wamp=options.trace)
   runner.run(ClientSession)
