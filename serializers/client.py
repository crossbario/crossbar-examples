import six
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor
from autobahn.twisted.wamp import ApplicationSession

class Client(ApplicationSession):

   @inlineCallbacks
   def onJoin(self, details):
      self.log.info("Client joined: {details}", details=details)
      self.log.info("\n\n*** Transport is using '{serializer}' serializer ***\n", serializer=self._transport._serializer.SERIALIZER_ID)

      try:
         res = yield self.call(u'com.example.add2', 2, 3)
         self.log.info("Procedure called with result: {res}", res=res)
      except:
         self.log.failure("Procedure call failed: {log_failure.value}")

      self.leave()

   def onLeave(self, details):
      self.log.info("Client left: {details}", details=details)
      self.disconnect()

   def onDisconnect(self):
      self.log.info("Client disconnected")
      reactor.stop()


if __name__ == '__main__':

   import sys
   import argparse

   parser = argparse.ArgumentParser()
   parser.add_argument('--realm', dest='realm', type=six.text_type, default=u'realm1', help='The realm to join. If not provided, let the router auto-choose the realm (default).')
   parser.add_argument('--url', dest='url', type=six.text_type, default=u'ws://localhost:8080/ws', help='The router URL (default: ws://localhost:8080/ws).')
   options = parser.parse_args()

   from autobahn.twisted.wamp import ApplicationRunner

   extra = {
   }

   runner = ApplicationRunner(url=options.url, realm=options.realm, extra=extra)
   runner.run(Client)
