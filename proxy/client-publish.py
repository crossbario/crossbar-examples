
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.component import Component, run
from autobahn.twisted.util import sleep
from autobahn.wamp.types import PublishOptions

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
            "serializers": ["json", "cbor"],
        },
    ],
    realm="realm1",
)

@comp.on_join
@inlineCallbacks
def _(session, details):
    print("joined: {}".format(session))
    topic_name = u"io.crossbar.demo.public.foo"

    while session.is_connected():
        print("publish to '{}'".format(topic_name))
        session.publish(
            topic_name, 1, 2, foo="bar",
            options=PublishOptions(exclude_me=False),
        )
        yield sleep(1)

if __name__ == "__main__":
    run([comp])#, log_level='debug')
