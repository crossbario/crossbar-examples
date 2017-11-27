import txaio
txaio.use_twisted()

import argparse
import os
import sys

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner


class ClientSession(ApplicationSession):

   def onConnect(self):
      print('Client session connected.')
      self.join(self.config.realm, [u'anonymous'])

   def onJoin(self, details):
      print('Client session joined: {}'.format(details))
      self.leave()

   def onLeave(self, details):
      print('Client session left: {}'.format(details))
      self.disconnect()

   def onDisconnect(self):
      print('Client session disconnected.')
      reactor.stop()


if __name__ == '__main__':

   parser = argparse.ArgumentParser()

   parser.add_argument("-d", "--debug", action="store_true",
                       help="Enable debug output.")

   parser.add_argument("--endpoint", default="tcp:127.0.0.1:8080",
                       help='WAMP client Twisted endpoint descriptor, e.g. "tcp:127.0.0.1:8080" or "unix:/tmp/mywebsocket".')

   parser.add_argument("--url", default=u"ws://localhost:8080/ws",
                       help='WAMP router URL (default: ws://localhost:8080/ws)')

   parser.add_argument("--realm", default=u"realm1",
                       help='WAMP realm (default: realm1)')

   args = parser.parse_args()

   if args.debug:
      txaio.start_logging(level='debug')
   else:
      txaio.start_logging(level='info')

   runner = ApplicationRunner(url=args.url, realm=args.realm)
   runner.run(ClientSession)
