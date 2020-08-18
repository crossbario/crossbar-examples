import os
import sys

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.types import PublishOptions
from autobahn.wamp import auth

if 'MYSECRET' in os.environ and len(sys.argv) > 1:
   # principal from command line, ticket from environment variable
   USER = sys.argv[1]
   USER_SECRET = os.environ['MYSECRET']
else:
   raise RuntimeError('missing authid or auth secret (from env var MYSECRET)')

print("User '{}' using secret '{}'".format(USER, USER_SECRET))


class ClientSession(ApplicationSession):

   def onConnect(self):
      print("Client session connected. Starting WAMP-CRA authentication on realm '{}' as user '{}' ..".format(self.config.realm, USER))
      self.join(self.config.realm, ["wampcra"], USER)

   def onChallenge(self, challenge):
      if challenge.method == "wampcra":
         print("WAMP-CRA challenge received: {}".format(challenge))

         if 'salt' in challenge.extra:
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
         res = yield self.call('com.example.add2', 2, 3)
         print("call result: {}".format(res))
      except Exception as e:
         print("call error: {}".format(e))

      ## (try to) register a procedure where we are not allowed to (so this should fail)
      ##
      try:
         reg = yield self.register(lambda x, y: x * y, 'com.example.mul2')
      except Exception as e:
         print("registration failed - this is expected: {}".format(e))

      ## publish to a couple of topics we are allowed to publish to.
      ##
      for topic in [
         'com.example.topic1',
         'com.foobar.topic1']:
         try:
            yield self.publish(topic, "hello", options = PublishOptions(acknowledge = True))
            print("ok, event published to topic {}".format(topic))
         except Exception as e:
            print("publication to topic {} failed: {}".format(topic, e))

      ## (try to) publish to a couple of topics we are not allowed to publish to (so this should fail)
      ##
      for topic in [
         'com.example.topic2',
         'com.foobar.topic2']:
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

   runner = ApplicationRunner(url='ws://localhost:8080/ws', realm='realm1')
   runner.run(ClientSession)
