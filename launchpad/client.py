###############################################################################
##
##  Copyright 2012 Tavendo GmbH. All rights reserved.
##
###############################################################################

import sys, time, random

from twisted.internet import reactor
print "Using Twisted reactor", reactor.__class__
print

from twisted.python import usage, log
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.websocket import connectWS
from autobahn.wamp import WampClientFactory, WampCraClientProtocol

import launchpad


BASEURI = "http://autobahn.tavendo.de/public/demo/launchpad#"


class LaunchpadOptions(usage.Options):
   optFlags = [['debug', 'd', 'Enable debug log messages.'],
               ['rpc', 'r', 'Forward pad presses as RPCs not PubSub events.']]
   optParameters = [
      ['wsuri', 'w', "ws://webmqtest.tavendo.de/ws", 'Tavendo WebMQ WebSocket endpoint.']
   ]


class LaunchpadClientProtocol(WampCraClientProtocol):

   def onSessionOpen(self):
      d = self.authenticate()
      d.addCallbacks(self.onAuthSuccess, self.onAuthError)


   def onClose(self, wasClean, code, reason):
      reactor.stop()


   def onAuthSuccess(self, permissions):
      print "WAMP session authenticated - permissions:", permissions
      self.subscribe(BASEURI + "light", self.onLight)
      self.subscribe(BASEURI + "reset", self.onReset)


   def onAuthError(self, e):
      uri, desc, details = e.value.args
      print "Authentication Error!", uri, desc, details


   def onLight(self, topic, event):
      print "onLight", event
      self.factory.launchpad.lp.light(event['x'], event['y'], event['r'], event['g'])


   def onReset(self, topic, event):
      print "onReset"
      self.factory.launchpad.lp.reset()


class LaunchpadClientFactory(WampClientFactory):

   def buildProtocol(self, addr):
      proto = LaunchpadClientProtocol()
      proto.factory = self
      self.launchpad.client = proto
      return proto


class LaunchpadConnector:

   def __init__(self):
      launchPads = launchpad.findLaunchpads()
      print launchPads
      self.lp = launchpad.launchpad(*launchPads[-1])
      self.lp.reset()
      self.client = None
      self.running = True

   def run(self):
      while self.running:
         e = self.lp.poll()
         if e:
            if self.padsAsRpcs:
               rpc = "http://example.com/test#onlaunchpad"
               print "RPC", rpc, e[0], e[1], 1 if e[2] else 0, e[3]
               if self.client:
                  reactor.callFromThread(self.client.call, rpc, e[0], e[1], 1 if e[2] else 0, e[3])
            else:
               topic = BASEURI + "pad"
               event = {'x': e[0], 'y': e[1], 'v': 1 if e[2] else 0, 't': e[3]}
               print "PUBSUB", topic, event
               if self.client:
                  reactor.callFromThread(self.client.publish, topic, event)
         time.sleep(0.01) # ok, since we're running in thread pool
      self.lp.reset()

   def stop(self):
      self.running = False


if __name__ == '__main__':

   ## parse options
   ##
   options = LaunchpadOptions()
   try:
      options.parseOptions()
   except usage.UsageError, errortext:
      print '%s %s' % (sys.argv[0], errortext)
      print 'Try %s --help for usage details' % sys.argv[0]
      sys.exit(1)

   log.startLogging(sys.stdout)

   wsuri = options.opts['wsuri']
   debug = True if options['debug'] else False
   padsAsRpcs = True if options['rpc'] else False

   ## MIDI connector to Launchpad
   ##
   launchpadConnector = LaunchpadConnector()
   launchpadConnector.padsAsRpcs = padsAsRpcs
   reactor.callInThread(launchpadConnector.run)

   ## WAMP client factory
   ##
   log.msg("Connecting to %s" % wsuri)
   wampClientFactory = LaunchpadClientFactory(wsuri, debugWamp = debug)
   wampClientFactory.launchpad = launchpadConnector
   connectWS(wampClientFactory)

   webdir = File(".")
   web = Site(webdir)
   reactor.listenTCP(8095, web)

   reactor.run()
