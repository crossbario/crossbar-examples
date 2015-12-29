from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession


class BackendSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

      def add2(x, y):
         print("add2() called with {} and {}".format(x, y))
         return x + y

      yield self.register(add2, 'com.example.add2')
      print("procedure add2() registered")
