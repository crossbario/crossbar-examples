import sys
import binascii
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.component import Component, run
from autobahn.twisted.util import sleep

TRANSPORT, SERIALIZER = sys.argv[1].split('-')
if TRANSPORT not in ['websocket', 'rawsocket']:
    raise Exception('invalid TRANSPORT "{}"'.format(TRANSPORT))
if SERIALIZER not in ['cbor', 'msgpack', 'json', 'ubjson']:
    raise Exception('invalid TRANSPORT "{}"'.format(TRANSPORT))

AUTHENTICATION = {
    'ticket': {
        'authid': 'user1',
        'ticket': 'secret1'
    }
}

if TRANSPORT == 'websocket':
    comp = Component(
        transports=[
            {
                "type": "websocket",
                "url": "ws://localhost:8443/ws",
                "endpoint": {
                    "type": "tcp",
                    "host": "localhost",
                    "port": 8443,
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
                "url": "rs://localhost:8443",
                "endpoint": {
                    "type": "tcp",
                    "host": "localhost",
                    "port": 8443,
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
    topic_name = u"demo.foo"

    def _foo(*args, **kwargs):
        print("{}: {} {}".format(topic_name, args, kwargs))
        assert 'foo' in kwargs and type(kwargs['foo']) == str and len(kwargs['foo']) == 22
        assert 'baz' in kwargs and type(kwargs['baz']) == bytes and len(kwargs['baz']) == 10
        assert binascii.a2b_hex(kwargs['foo'][2:]) == kwargs['baz']

    session.subscribe(_foo, topic_name)
    print("subscribed")
    while session.is_connected():
        print(".")
        yield sleep(1)

if __name__ == "__main__":
    run([comp], log_level='debug')
