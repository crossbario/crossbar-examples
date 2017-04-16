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


if False:
    # topic we subscribe to. this will be subscribed to with prefix matching policy
    SUBTOPIC = u'mqtt.test.mytopic.'
    SUBMATCH = u'prefix'
else:
    # topic we subscribe to. this contains empty path components (".."),
    # and will be subscribed to with wildcard matching policy
    SUBTOPIC = u'mqtt..mytopic.'
    SUBMATCH = u'wildcard'

# this is the topic prefix we are publishing to: we will append an integer (as str)
PUBTOPIC1 = u'mqtt.test.mytopic.{}'
PUBTOPIC2 = u'mqtt.foobar.mytopic.{}'
PUBTOPIC3 = u'mqtt.{}.mytopic.something'
PUBTOPIC4 = u'bar.test.mytopic.{}'


class MySession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info('session joined: {details}', details=details)

        def on_event(pid, seq, ran, details=None):
            self.log.info('event received on topic {topic}: pid={pid}, seq={seq}, ran={ran}, details={details}\n', topic=details.topic, pid=pid, seq=seq, ran=binascii.b2a_hex(ran), details=details)

        reg = yield self.subscribe(on_event,
                                   SUBTOPIC,
                                   options=SubscribeOptions(match=SUBMATCH, details=True))

        self.log.info('subscribed to topic {topic} (match={match}): registration={reg}', topic=SUBTOPIC, match=SUBMATCH, reg=reg)

        pid = os.getpid()
        seq = 1

        while True:
            self.log.info('-' * 60)
            pubs = []
            for PUBTOPIC in [PUBTOPIC1, PUBTOPIC2, PUBTOPIC3, PUBTOPIC4]:
                topic = PUBTOPIC.format(seq)
                pub = self.publish(
                    topic,
                    pid, seq, os.urandom(8),
                    options=PublishOptions(acknowledge=True, exclude_me=False),
                )
                self.log.info('event published to {topic}: publication={pub}\n', topic=topic, pub=pub)
                pubs.append(pub)
            seq += 1
            yield txaio.gather(pubs)
            yield sleep(1)


if __name__ == '__main__':
    txaio.start_logging(level='info')
    runner = ApplicationRunner(u'rs://localhost:8080', u'realm1')
#    runner = ApplicationRunner(u'ws://localhost:8080/ws', u'realm1')
    runner.run(MySession)
