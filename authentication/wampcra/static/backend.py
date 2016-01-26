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

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession


class BackendSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
      print("Backend session joined: {}".format(details))

      def onhello(msg=None):
         print("event received on {}: {}".format(topic, msg))

      ## SUBSCRIBE to a few topics we are allowed to subscribe to.
      ##
      for topic in [
         u'com.example.topic1',
         u'com.foobar.topic1',
         u'com.foobar.topic2']:

         try:
            sub = yield self.subscribe(onhello, topic)
            print("ok, subscribed to topic {}".format(topic))
         except Exception as e:
            print("could not subscribe to {}: {}".format(topic, e))

      ## (try to) SUBSCRIBE to a topic we are not allowed to subscribe to (so this should fail).
      ##
      try:
         sub = yield self.subscribe(onhello, u'com.example.topic2')
      except Exception as e:
         print("subscription failed (this is expected!) {}".format(e))

      ## REGISTER a procedure for remote calling
      ##
      def add2(x, y):
         print("add2() called with {} and {}".format(x, y))
         return x + y

      try:
         reg = yield self.register(add2, u'com.example.add2')
         print("procedure add2() registered")
      except Exception as e:
         print("could not register procedure: {}".format(e))
