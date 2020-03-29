
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

    def _foo(*args, **kw):
        print("{}: {} {}".format(topic_name, args, kw))

    session.subscribe(_foo, topic_name)
    print("subscribed")
    while session.is_connected():
        print(".")
        yield sleep(1)

if __name__ == "__main__":
    run([comp])#, log_level='debug')
