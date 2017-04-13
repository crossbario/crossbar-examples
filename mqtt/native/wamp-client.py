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

from autobahn.wamp.types import PublishOptions, SubscribeOptions

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

# topic we publish and subscribe to
TOPIC = u'mqtt.test.mytopic1'


class MySession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info('session joined: {details}', details=details)

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
