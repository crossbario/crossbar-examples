import sys
import binascii
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.component import Component, run
from autobahn.twisted.util import sleep
from autobahn.wamp.types import SubscribeOptions

AUTHMETHOD, TRANSPORT, SERIALIZER = sys.argv[1].split('-')
if AUTHMETHOD not in ['anonymous', 'ticket']:
    raise Exception('invalid AUTHMETHOD "{}"'.format(AUTHMETHOD))
if TRANSPORT not in ['websocket', 'rawsocket']:
    raise Exception('invalid TRANSPORT "{}"'.format(TRANSPORT))
if SERIALIZER not in ['cbor', 'msgpack', 'json', 'ubjson']:
    raise Exception('invalid TRANSPORT "{}"'.format(TRANSPORT))

if AUTHMETHOD == 'ticket':
    AUTHENTICATION = {
        'ticket': {
            'authid': 'user1',
            'ticket': 'secret1'
        }
    }
elif AUTHMETHOD == 'anonymous':
    AUTHENTICATION = None

if TRANSPORT == 'websocket':
    comp = Component(
        transports=[
            {
                "type": "websocket",
                "url": "ws://localhost:8080/ws",
                "endpoint": {
                    "type": "tcp",
                    "host": "localhost",
                    "port": 8080,
                },
                "serializers": [SERIALIZER],
            },
        ],
        realm="realm1",
        authentication=AUTHENTICATION
    )
elif TRANSPORT == 'rawsocket':
    comp = Component(
        transports=[
            {
                "type": "rawsocket",
                "url": "rs://localhost:8080",
                "endpoint": {
                    "type": "tcp",
                    "host": "localhost",
                    "port": 8080,
                },
                "serializer": SERIALIZER,
            },
        ],
        realm="realm1",
        authentication=AUTHENTICATION
    )


@comp.on_join
@inlineCallbacks
def _(session, details):
    print("joined: {}".format(details))
    if details.authmethod == 'anonymous':
        topic_name = "io.crossbar.demo.public."
    else:
        topic_name = "io.crossbar.demo."

    def _foo(*args, **kwargs):
        print("{}: {} {}".format(topic_name, args, kwargs))
        assert 'foo' in kwargs and type(kwargs['foo']) == str and len(kwargs['foo']) == 22
        assert 'baz' in kwargs and type(kwargs['baz']) == bytes and len(kwargs['baz']) == 10
        assert binascii.a2b_hex(kwargs['foo'][2:]) == kwargs['baz']

    yield session.subscribe(_foo, topic_name, options=SubscribeOptions(match='prefix'))
    print("subscribed")
    while session.is_connected():
        print(".")
        yield sleep(1)


if __name__ == "__main__":
    run([comp], log_level='info')
