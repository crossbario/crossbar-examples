#
# Example WAMP client, interoperating with the MQTT client
#
# Note that the example is slightly verbose, to show more
# features and with extensive logging
#

import txaio
txaio.use_twisted()

import os
import struct
import binascii

from twisted.internet.defer import inlineCallbacks

from autobahn.wamp.types import PublishOptions, SubscribeOptions,EncodedPayload
from autobahn.wamp.interfaces import IPayloadCodec

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

# topic we publish and subscribe to
TOPIC = u'mqtt.test.mytopic1'


class MyCodec(object):
    """
    Our codec to encode/decode our custom binary payload. This is needed
    in "payload transparency mode" (a WAMP AP / Crossbar.io feature), so
    the app code is shielded, so you can write your code as usual in Autobahn/WAMP.
    """

    # binary payload format we use in this example:
    # unsigned short + signed int + 8 bytes (all big endian)
    FORMAT = '>Hl8s'

    def encode(self, is_originating, uri, args=None, kwargs=None):
        # Autobahn wants to send custom payload: convert to an instance
        # of EncodedPayload
        payload = struct.pack(self.FORMAT, args[0], args[1], args[2])
        return EncodedPayload(payload, u'mqtt')

    def decode(self, is_originating, uri, encoded_payload):
        # Autobahn has received a custom payload.
        # convert it into a tuple: (uri, args, kwargs)
        return uri, struct.unpack(self.FORMAT, encoded_payload.payload), None

# we need to register our codec!
IPayloadCodec.register(MyCodec)


class MySession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info('session joined: {details}', details=details)

        # this is the one and only line of code that is different from a regular
        # WAMP app session: we set our codec, and everything else is transparent (!)
        self.set_payload_codec(MyCodec())

        def on_event(pid, seq, ran, details=None):
            self.log.info('event received on topic {topic}: pid={pid}, seq={seq}, ran={ran}, details={details}\n', topic=TOPIC, pid=pid, seq=seq, ran=binascii.b2a_hex(ran), details=details)

        reg = yield self.subscribe(on_event, TOPIC, options=SubscribeOptions(details=True))

        self.log.info('subscribed to topic {topic}: registration={reg}', topic=TOPIC, reg=reg)

        pid = os.getpid()
        seq = 1

        while True:
            pub = yield self.publish(
                TOPIC,
                pid, seq, os.urandom(8),
                options=PublishOptions(acknowledge=True, exclude_me=False),
            )
            self.log.info('event published: publication={pub}\n', pub=pub)
            seq += 1
            yield sleep(1)


if __name__ == '__main__':
    txaio.start_logging(level='info')
    runner = ApplicationRunner(u'rs://localhost:8080', u'realm1')
#    runner = ApplicationRunner(u'ws://localhost:8080/ws', u'realm1')
    runner.run(MySession)
