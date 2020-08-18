from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession


class BackendSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
      print("Backend session joined: {}".format(details))

      def onhello(msg):
         print("event received on {}: {}".format(topic, msg))

      ## SUBSCRIBE to a few topics we are allowed to subscribe to.
      ##
      for topic in [
         'com.example.topic1',
         'com.foobar.topic1',
         'com.foobar.topic2']:

         try:
            sub = yield self.subscribe(onhello, topic)
            print("ok, subscribed to topic {}".format(topic))
         except Exception as e:
            print("could not subscribe to {}: {}".format(topic, e))

      ## (try to) SUBSCRIBE to a topic we are not allowed to subscribe to (so this should fail).
      ##
      try:
         sub = yield self.subscribe(onhello, 'com.example.topic2')
      except Exception as e:
         print("subscription failed (this is expected!) {}".format(e))

      ## REGISTER a procedure for remote calling
      ##
      def add2(x, y):
         print("add2() called with {} and {}".format(x, y))
         return x + y

      try:
         reg = yield self.register(add2, 'com.example.add2')
         print("procedure add2() registered")
      except Exception as e:
         print("could not register procedure: {}".format(e))
