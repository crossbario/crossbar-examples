from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession


class MyCodec(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        def decode(mapped_topic, topic, payload):
            options = {
                'args': None,
                'kwargs': None
            }
            return options

        def encode(mapped_topic, topic, args, kwargs):
            payload = b''
            return payload

        prefix = u'com.example.mqtt'

        yield self.register(decode, u'{}.decode'.format(prefix))
        yield self.register(encode, u'{}.encode'.format(prefix))

        self.log.info("MyCodec ready!")
