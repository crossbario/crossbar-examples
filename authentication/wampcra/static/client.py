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
import sys

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.types import PublishOptions
from autobahn.wamp import auth

if 'MYSECRET' in os.environ and len(sys.argv) > 1:
   # user from command line, secret from environment variable
   USER = sys.argv[1].decode('utf8')
   USER_SECRET = os.environ['MYSECRET'].decode('utf8')
else:
   # less good: user, including secret hard-coded
   USER = u'peter'
   USER_SECRET = u'secret1'


class ClientSession(ApplicationSession):

   def onConnect(self):
      print("Client session connected. Starting WAMP-CRA authentication on realm '{}' as user '{}' ..".format(self.config.realm, USER))
      self.join(self.config.realm, [u"wampcra"], USER)

   def onChallenge(self, challenge):
      if challenge.method == u"wampcra":
         print("WAMP-CRA challenge received: {}".format(challenge))

         if u'salt' in challenge.extra:
            # salted secret
            key = auth.derive_key(USER_SECRET,
                                  challenge.extra['salt'],
                                  challenge.extra['iterations'],
                                  challenge.extra['keylen'])
         else:
            # plain, unsalted secret
            key = USER_SECRET

         # compute signature for challenge, using the key
         signature = auth.compute_wcs(key, challenge.extra['challenge'])

         # return the signature to the router for verification
         return signature

      else:
         raise Exception("Invalid authmethod {}".format(challenge.method))

   @inlineCallbacks
   def onJoin(self, details):
      print("Client session joined: {}".format(details))

      ## call a procedure we are allowed to call (so this should succeed)
      ##
      try:
         res = yield self.call(u'com.example.add2', 2, 3)
         print("call result: {}".format(res))
      except Exception as e:
         print("call error: {}".format(e))

      ## (try to) register a procedure where we are not allowed to (so this should fail)
      ##
      try:
         reg = yield self.register(lambda x, y: x * y, u'com.example.mul2')
      except Exception as e:
         print("registration failed - this is expected: {}".format(e))

      ## publish to a couple of topics we are allowed to publish to.
      ##
      for topic in [
         u'com.example.topic1',
         u'com.foobar.topic1']:
         try:
            yield self.publish(topic, "hello", options = PublishOptions(acknowledge = True))
            print("ok, event published to topic {}".format(topic))
         except Exception as e:
            print("publication to topic {} failed: {}".format(topic, e))

      ## (try to) publish to a couple of topics we are not allowed to publish to (so this should fail)
      ##
      for topic in [
         u'com.example.topic2',
         u'com.foobar.topic2']:
         try:
            yield self.publish(topic, "hello", options = PublishOptions(acknowledge = True))
            print("ok, event published to topic {}".format(topic))
         except Exception as e:
            print("publication to topic {} failed - this is expected: {}".format(topic, e))

      self.leave()

   def onLeave(self, details):
      print("Client session left: {}".format(details))
      self.disconnect()

   def onDisconnect(self):
      print("Client session disconnected.")
      reactor.stop()


if __name__ == '__main__':

   from autobahn.twisted.wamp import ApplicationRunner

   runner = ApplicationRunner(url=u'ws://localhost:8080/ws', realm=u'realm1')
   runner.run(ClientSession)
