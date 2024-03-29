import os
import sys

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.types import PublishOptions

if 'MYTICKET' in os.environ and len(sys.argv) > 1:
   # principal from command line, ticket from environment variable
   PRINCIPAL = sys.argv[1]
   PRINCIPAL_TICKET = os.environ['MYTICKET']
else:
   raise RuntimeError('missing authid or auth secret (from env var MYTICKET)')

print("Principal '{}' using ticket '{}'".format(PRINCIPAL, PRINCIPAL_TICKET))


class ClientSession(ApplicationSession):

   def onConnect(self):
      print("Client session connected. Starting WAMP-Ticket authentication on realm '{}' as principal '{}' ..".format(self.config.realm, PRINCIPAL))
      self.join(self.config.realm, ["ticket"], PRINCIPAL)

   def onChallenge(self, challenge):
      if challenge.method == "ticket":
         print("WAMP-Ticket challenge received: {}".format(challenge))
         return PRINCIPAL_TICKET
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
         print("registration failed (this is expected!) {}".format(e))

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
            print("publication to topic {} failed (this is expected!) {}".format(topic, e))

      self.leave()

   def onLeave(self, details):
      print("Client session left: {}".format(details))
      self.config.extra['exit_details'] = details
      self.disconnect()

   def onDisconnect(self):
      print("Client session disconnected.")
      reactor.stop()


if __name__ == '__main__':

   from autobahn.twisted.wamp import ApplicationRunner

   extra = {
      'exit_details': None,
   }

   runner = ApplicationRunner(url='ws://localhost:8080/ws', realm='realm1', extra=extra)
   runner.run(ClientSession)

   # CloseDetails(reason=<wamp.error.not_authorized>, message='WAMP-CRA signature is invalid')
   print(extra['exit_details'])

   if extra['exit_details'].reason != 'wamp.close.normal':
      sys.exit(1)
   else:
      sys.exit(0)
