import six
import argparse

import txaio
txaio.use_twisted()

from autobahn.twisted.util import sleep
from autobahn.wamp.types import PublishOptions
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.serializer import JsonSerializer, CBORSerializer, MsgPackSerializer


class ClientSession(ApplicationSession):

   async def onJoin(self, details):
      print('Client session joined: {}'.format(details))

      topic = 'com.example.topic1'

      def on_event(i):
         print('Event received: {}'.format(i))

      await self.subscribe(on_event, topic)

      for i in range(5):
         self.publish(topic, i, options=PublishOptions(acknowledge=True, exclude_me=False))
         await sleep(1)

      self.leave()

   def onLeave(self, details):
       print('Client session left: {}'.format(details))
       self.config.runner.stop()
       self.disconnect()

   def onDisconnect(self):
      print('Client session disconnected.')
      from twisted.internet import reactor
      reactor.stop()


if __name__ == '__main__':

   parser = argparse.ArgumentParser()

   parser.add_argument('-d',
                       '--debug',
                       action='store_true',
                       help='Enable debug output.')

   parser.add_argument('--url',
                       dest='url',
                       type=six.text_type,
                       default="ws://localhost:8080/ws",
                       help='The router URL, eg "ws://localhost:8080/ws" or "rs://localhost:8081" (default: "ws://localhost:8080/ws").')

   parser.add_argument('--realm',
                       dest='realm',
                       type=six.text_type,
                       default="realm1",
                       help='The realm to join (default: "realm1").')

   parser.add_argument('--serializer',
                       dest='serializer',
                       type=six.text_type,
                       default="json",
                       help='Serializer to use, one of "json", "cbor", "msgpack", "all" or "unspecified" (default: "unspecified")')

   args = parser.parse_args()

   # start logging
   if args.debug:
      txaio.start_logging(level='debug')
   else:
      txaio.start_logging(level='info')

   # explicitly select serializer
   if args.serializer == 'unspecified':
      serializers = None
   else:
      serializers = []

      if args.serializer in ['cbor', 'all']:
         serializers.append(CBORSerializer())

      if args.serializer in ['msgpack', 'all']:
         serializers.append(MsgPackSerializer())

      if args.serializer in ['json', 'all']:
         serializers.append(JsonSerializer())

   # any extra info we want to forward to our ClientSession (in self.config.extra)
   extra = {}

   # now actually run a WAMP client using our session class ClientSession
   runner = ApplicationRunner(url=args.url, realm=args.realm, extra=extra, serializers=serializers)
   runner.run(ClientSession, auto_reconnect=True)
