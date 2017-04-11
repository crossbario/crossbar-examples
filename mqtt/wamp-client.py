import txaio
txaio.use_twisted()

import os
import struct

from twisted.internet.defer import inlineCallbacks

from autobahn.wamp.types import PublishOptions, EncodedPayload
from autobahn.wamp.interfaces import IPayloadCodec

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

TOPIC = u'mqtt.test.mytopic1'


class MyCodec(object):

    FORMAT = '<Hl'

    def encode(self, is_originating, uri, args=None, kwargs=None):
        payload = struct.pack(self.FORMAT, args[0], args[1])
        return EncodedPayload(payload, u'mqtt')

    def decode(self, is_originating, uri, encoded_payload):
        return uri, struct.unpack(self.FORMAT, encoded_payload.payload), None

IPayloadCodec.register(MyCodec)


class MySession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info('session joined: {details}', details=details)

        self.set_payload_codec(MyCodec())

        def on_event(pid, seq):
            self.log.info('event received on topic {topic}: pid={pid}, seq={seq}', topic=TOPIC, pid=pid, seq=seq)

        yield self.subscribe(on_event, TOPIC)

        self.log.info('subscribed to topic {topic}', topic=TOPIC)

        pid = os.getpid()
        seq = 1

        while True:
            yield self.publish(
                TOPIC,
                pid, seq,
                options=PublishOptions(acknowledge=True, exclude_me=False),
            )
            seq += 1
            yield sleep(1)


if __name__ == '__main__':
    txaio.start_logging(level='info')
    runner = ApplicationRunner(u'ws://localhost:8080/ws', u'realm1')
    runner.run(MySession, auto_reconnect=True)
