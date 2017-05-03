from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession

import struct
import binascii

# binary payload format we use in this example:
# unsigned short + signed int + 8 bytes (all big endian)
FORMAT = '>Hl8s'


class MyCodec(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        def decode(mapped_topic, topic, payload):
            if mapped_topic.startswith(u'mqtt'):
                pid, seq, ran = struct.unpack(FORMAT, payload)
                options = {
                    'args': [pid, seq, ran]
                }
            else:
                options = {
                    'args': [payload.decode('utf8')]
                }
            self.log.info('MyCodec.decode "{topic}": from_mqtt={from_mqtt} -> to_wamp={to_wamp}', topic=topic, from_mqtt=payload, to_wamp=options)
            return options

        def encode(mapped_topic, topic, args, kwargs):
            if topic.startswith(u'mqtt'):
                pid, seq, ran = args
                payload = struct.pack(FORMAT, pid, seq, ran)
            else:
                payload = args[0].encode('utf8')
            self.log.info('MyCodec.encode "{topic}": from_wamp={from_wamp} -> to_mqtt={to_mqtt}', topic=topic, from_wamp={u'args': args}, to_mqtt=payload)
            return payload

        prefix = u'com.example.mqtt'

        yield self.register(decode, u'{}.decode'.format(prefix))
        yield self.register(encode, u'{}.encode'.format(prefix))

        self.log.info("MyCodec ready!")
