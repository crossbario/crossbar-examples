
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
    ]
)

@comp.on_join
@inlineCallbacks
def _(session, details):
    print("joined: {}".format(session))

    def _foo(*args, **kw):
        print("foo: {} {}".format(args, kw))

    topic_name = "io.crossbar.demo.public.foo"
    session.subscribe(_foo, topic_name)
    print("subscribed")
    while True:
        print("publish to '{}'".format(topic_name))
        session.publish(
            topic_name, 1, 2, foo="bar",
            options=PublishOptions(exclude_me=False),
        )
        yield sleep(1)

if __name__ == "__main__":
    run([comp])#, log_level='debug')
