###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Tavendo GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

from __future__ import print_function

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.types import SubscribeOptions, RegisterOptions
from autobahn.wamp.keyring import KeyRing, Key

from sample_keys import RESPONDER_PRIV, ORIGINATOR_PUB


class Component(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        print("joined")

        keyring = KeyRing()
        key = Key(responder_priv=RESPONDER_PRIV, originator_pub=ORIGINATOR_PUB)
        keyring.set_key(u'com.myapp.encrypted.', key)
        self.set_keyring(keyring)

        def add2(a, b, details=None):
            print("call received: a={}, b={}, details={}".format(a, b, details))
            return a + b

        options = RegisterOptions(details_arg='details')
        reg1 = yield self.register(add2, u'com.myapp.add2', options=options)
        reg2 = yield self.register(add2, u'com.myapp.encrypted.add2', options=options)


        def on_hello(msg, details=None):
            print("event received: msg='{}', details={}".format(msg, details))

        options = SubscribeOptions(details_arg='details')
        sub1 = yield self.subscribe(on_hello, u'com.myapp.hello', options=options)
        sub2 = yield self.subscribe(on_hello, u'com.myapp.encrypted.hello', options=options)

        print("ready!")

    def onLeave(self, details):
        self.disconnect()

    def onDisconnect(self):
        from twisted.internet import reactor
        reactor.stop()


if __name__ == '__main__':
    runner = ApplicationRunner(u"ws://127.0.0.1:8080", u"realm1")
    runner.run(Component)
