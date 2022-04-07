import os
import sys
import binascii
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.component import Component, run
from autobahn.twisted.util import sleep
from autobahn.wamp.types import PublishOptions

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
            'authid': 'user2',
            'ticket': 'secret2'
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
        topic_name = "io.crossbar.demo.public.foo"
    else:
        topic_name = "io.crossbar.demo.user.foo"
    pid = os.getpid()
    counter = 0

    while session.is_connected():
        print("pid {} publish {} to '{}'".format(pid, counter, topic_name))
        data = os.urandom(10)
        yield session.publish(
            topic_name, pid, counter, foo='0x'+binascii.b2a_hex(data).decode(), baz=data,
            options=PublishOptions(acknowledge=True, exclude_me=False),
        )
        counter += 1
        yield sleep(1)


if __name__ == "__main__":
    run([comp], log_level='info')
