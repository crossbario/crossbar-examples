from twisted.logger import Logger
from twisted.internet.defer import Deferred, inlineCallbacks

from autobahn.wamp.types import SubscribeOptions
from autobahn.wamp.exception import ApplicationError

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationRunner
from autobahn.twisted.wamp import ApplicationSession


class Bridge(ApplicationSession):

    @inlineCallbacks
    def _setup_event_forwarding(self, other):

        print("setup event forwarding between {} and {} ..".format(self, other))

        self._subs = {}

        # listen to when new subscriptions are created on the router
        #
        @inlineCallbacks
        def on_subscription_create(sub_id, sub_details, details=None):
            print(self, sub_id, sub_details, details)

            self._subs[sub_id] = sub_details

            uri = sub_details['uri']

            def on_event(*args, **kwargs):
                print("forwarding event from {} to {}".format(other, self))
                details = kwargs.pop('details')
                self.publish(uri, *args, **kwargs)

            sub = yield other.subscribe(on_event, uri, options=SubscribeOptions(details_arg="details"))
            self._subs[sub_id]['sub'] = sub

            print("{} subscribed to {}".format(other, uri))

        yield self.subscribe(on_subscription_create, u"wamp.subscription.on_create", options=SubscribeOptions(details_arg="details"))

        # listen to when a subscription is removed from the router
        #
        @inlineCallbacks
        def on_subscription_delete(session_id, sub_id, details=None):
            print(self, session_id, sub_id, details)

            sub_details = self._subs.get(sub_id, None)
            if not sub_details:
                print("subscription not tracked - huh??")
                return

            uri = sub_details['uri']

            yield self._subs[sub_id]['sub'].unsubscribe()

            del self._subs[sub_id]

            print("{} unsubscribed from {}".format(other, uri))

        yield self.subscribe(on_subscription_delete, u"wamp.subscription.on_delete", options=SubscribeOptions(details_arg="details"))

        # get current subscriptions on the router
        #
        subs = yield self.call(u"wamp.subscription.list")
        for sub_id in subs['exact']:
            sub = yield self.call(u"wamp.subscription.get", sub_id)
            yield on_subscription_create(sub['id'], sub)

        print("event forwarding setup done.")


class EdgeBridge(Bridge):

    @inlineCallbacks
    def onJoin(self, details):
        print("EdgeBridge joined: {}".format(details))

        core_session = self.config.extra['core']

        yield self._setup_event_forwarding(core_session)

        if self.config and 'onready' in self.config.extra:
            self.config.extra['onready'].callback(self)

        print("EdgeBridge ready")


class CoreBridge(Bridge):

    @inlineCallbacks
    def onJoin(self, details):
        print("CoreBridge joined: {}".format(details))

        extra = {
            'onready': Deferred(),
            'core': self
        }
        runner = ApplicationRunner(url=self.config.extra['edge'], realm=details.realm, extra=extra)
        runner.run(EdgeBridge, start_reactor=False)

        edge_session = yield extra['onready']

        yield self._setup_event_forwarding(edge_session)

        if self.config and 'onready' in self.config.extra:
            self.config.extra['onready'].callback(self)

        print("CoreBridge ready")


class TestBridge(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        print("Test session ready: {}".format(details))

        uri = u"com.example.onhello"

        def on_event(msg):
            print("got event", msg)
            #details = kwargs.pop('details')
            #self.publish(uri, *args, **kwargs)

        #sub = yield self.subscribe(on_event, uri, options=SubscribeOptions(details_arg="details"))
        sub = yield self.subscribe(on_event, uri)
        print(self, "subscribed to", uri, sub)


class AppSession(ApplicationSession):

    log = Logger()

    @inlineCallbacks
    def onJoin(self, details):

        # SUBSCRIBE to a topic and receive events
        #
        def onhello(msg):
            self.log.info("event for 'onhello' received: {msg}", msg=msg)

        yield self.subscribe(onhello, 'com.example.onhello')
        self.log.info("subscribed to topic 'onhello'")



if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--core',
        dest='core',
        type=unicode,
        help='The URL of the core router.')

    parser.add_argument('--edge',
        dest='edge',
        type=unicode,
        help='The URL of the edge router.')

    parser.add_argument('--realm',
        dest='realm',
        type=unicode,
        help='The WAMP realm to join.')

    options = parser.parse_args()

    extra = {
        'edge': options.edge
    }

    runner = ApplicationRunner(url=options.core, realm=options.realm, extra=extra)
    runner.run(CoreBridge)
#    runner.run(TestBridge)
#    runner.run(AppSession)
