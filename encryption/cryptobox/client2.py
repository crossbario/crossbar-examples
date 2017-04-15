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


import txaio
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.types import SubscribeOptions, RegisterOptions
from autobahn.wamp.cryptobox import KeyRing, Key
from autobahn.wamp.exception import ApplicationError

from sample_keys import PRIVKEY, RESPONDER_PRIV, ORIGINATOR_PUB


class Component2(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info('session joined: {details}', details=details)

        # setup application payload end-to-end encryption ("WAMP-cryptobox")
        # when a keyring was set, end-to-end encryption is performed automatically
        if False:
            # this is simplest keyring: for all URIs, use one key for both
            # originators and responders.
            keyring = KeyRing(PRIVKEY)
        else:
            # this is a more specialized keyring: we only make URIs starting
            # with "com.myapp.encrypted." encrypted, and only with private key
            # for originator (= this session, as it is "calling" and "publishing")
            keyring = KeyRing()

            # since we want to act as "callee" and "subscriber") we are thus a "responder"
            # and responders need the responder private key. however, we don't act as "callers"
            # or "publishers", and hence can get away with the public key for the originator only!
            key = Key(originator_pub=ORIGINATOR_PUB, responder_priv=RESPONDER_PRIV)
            keyring.set_key(u'com.myapp.encrypted.', key)

        self.set_payload_codec(keyring)

        # now start the testing ..

        def add2(a, b, details=None):
            self.log.info('call received: a={a}, b={b}, details={details}', a=a, b=b, details=details)

            # when the procedure args were encrypted, the result will be always encrypted too!
            return a + b

        options = RegisterOptions(details_arg='details')
        reg1 = yield self.register(add2, u'com.myapp.add2', options=options)
        reg2 = yield self.register(add2, u'com.myapp.encrypted.add2', options=options)

        def failme(encrypted_error, details=None):
            # IMPORTANT: independent of whether the "failme" procedure args were encrypted or not,
            # an error returned to the caller will be encrypted or not depending soley
            # on the error URI!
            if encrypted_error:
                raise ApplicationError(u"com.myapp.encrypted.error1", custom1=23, custom2=u'Hello')
            else:
                raise ApplicationError(u"com.myapp.error1", custom1=23, custom2=u'Hello')

        reg3 = yield self.register(failme, u'com.myapp.failme', options=options)
        reg4 = yield self.register(failme, u'com.myapp.encrypted.failme', options=options)

        def on_hello(msg, details=None):
            self.log.info('event received: msg="{msg}", details={details}', msg=msg, details=details)

        options = SubscribeOptions(details=True)
        sub1 = yield self.subscribe(on_hello, u'com.myapp.hello', options=options)
        sub2 = yield self.subscribe(on_hello, u'com.myapp.encrypted.hello', options=options)

        self.log.info('session ready!')

    def onLeave(self, details):
        self.log.info('session left: {details}',details=details)
        ApplicationSession.onLeave(self, details)

    def onDisconnect(self):
        ApplicationSession.onDisconnect(self)
        from twisted.internet import reactor
        reactor.stop()


if __name__ == '__main__':
    txaio.start_logging(level='info')
    runner = ApplicationRunner(u"ws://127.0.0.1:8080", u"realm1")
    runner.run(Component2)
