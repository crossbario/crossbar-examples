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

import txaio
txaio.use_twisted()

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.types import PublishOptions, CallOptions
from autobahn.wamp.exception import ApplicationError
from autobahn.wamp.cryptobox import KeyRing, Key

from sample_keys import PRIVKEY, ORIGINATOR_PRIV, RESPONDER_PUB


class Component1(ApplicationSession):

    NUM = 3

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

            # we need to have a keyring first. create an empty one.
            keyring = KeyRing()

            # since we want to act as "caller" and "publisher", we are thus a "originator"
            # and originators need the originator private key. however, we don't act as "callees"
            # or "subscribers", and hence can get away with the public key for the responder only!
            key = Key(originator_priv=ORIGINATOR_PRIV, responder_pub=RESPONDER_PUB)

            # we now associate URIs starting with "com.myapp.encrypted." with the
            # encryption keys ..
            keyring.set_key(u'com.myapp.encrypted.', key)

        # .. and finally set the keyring on the session. from now on, all calls (and event)
        # on URIs that start with "com.myapp.encrypted." will be encrypted. Calls (and events)
        # on URIs different from that will continue to travel unencrypted!
        self.set_payload_codec(keyring)

        # now start the testing ..

        yield self._test_rpc()
        yield self._test_rpc_errors()
        yield self._test_pubsub()

        self.log.info('done!')
        self.leave()

    @inlineCallbacks
    def _test_rpc(self, delay=None):
        options = CallOptions()

        counter = 1
        while counter <= self.NUM:
            for proc in [u'com.myapp.add2',
                         u'com.myapp.encrypted.add2']:
                try:
                    res = yield self.call(proc, 23, counter, options=options)
                    self.log.info('{proc} call result: {res}', proc=proc, res=res)
                except Exception as e:
                    self.log.info('{proc} call error: {e}', proc=proc, e=e)

            if delay:
                yield sleep(delay)
            counter += 1

    @inlineCallbacks
    def _test_rpc_errors(self):
        options = CallOptions()

        for proc, encrypted_error in [(u'com.myapp.failme', False),
                                      (u'com.myapp.failme', True),
                                      (u'com.myapp.encrypted.failme', False),
                                      (u'com.myapp.encrypted.failme', True)]:
            try:
                res = yield self.call(proc, encrypted_error, options=options)
                self.log.info('{proc} called with encrypted_error={encrypted_error} - result: {res}', proc=proc, encrypted_error=encrypted_error, res=res)
            except Exception as e:
                self.log.info('{proc} called with encrypted_error={encrypted_error} - error: {e}', proc=proc, encrypted_error=encrypted_error, e=e)

    @inlineCallbacks
    def _test_pubsub(self, delay=None):
        options = PublishOptions(acknowledge=True, exclude_me=False)
        counter = 1
        while counter <= self.NUM:
            msg = u'Counter is at {}'.format(counter)

            topic = u'com.myapp.hello'
            pub = yield self.publish(topic, msg, options=options)
            self.log.info('event published: {pub}', pub=pub)

            topic = u'com.myapp.encrypted.hello'
            pub = yield self.publish(topic, msg, options=options)
            self.log.info('event published: {pub}', pub=pub)

            if delay:
                yield sleep(1)
            counter += 1

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
    runner.run(Component1)
