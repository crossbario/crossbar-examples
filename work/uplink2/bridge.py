from twisted.internet.defer import Deferred, inlineCallbacks
from autobahn.twisted.wamp import ApplicationRunner
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.types import SubscribeOptions

#((6601561172300290, {u'created': u'2015-11-27T17:15:16.170Z', u'uri': u'com.example.on_hello', u'match': u'exact', u'id': 371735546863363}), {}, <autobahn.wamp.types.EventDetails object at 0x2b0c8b83d5d0>)

class EdgeBridge(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        print("EdgeBridge session ready: {}".format(details))

        other_session = self.config.extra['core']

        # setup event forwarding
        #
        @inlineCallbacks
        def on_subscription_create(sub, sub_details, details=None):
            print(sub, sub_details, details)

            uri = sub_details['uri']

            def on_event(*args, **kwargs):
                details = kwargs.pop('details')
                self.publish(uri, *args, **kwargs)

            yield other_session.subscribe(on_event, uri)

        yield self.subscribe(on_subscription_create, u"wamp.subscription.on_create", options=SubscribeOptions(details_arg="details"))

        # signal readiness
        #
        self.config.extra['onready'].callback(self)


class CoreBridge(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        print("CoreBridge session ready: {}".format(details))

        extra = {
            'onready': Deferred(),
            'core': self
        }
        runner = ApplicationRunner(url=self.config.extra['edge'], realm=details.realm, extra=extra)
        runner.run(EdgeBridge, start_reactor=False)

        other_session = yield extra['onready']

        # setup event forwarding
        #
        @inlineCallbacks
        def on_subscription_create(sub, sub_details, details=None):
            print(sub, sub_details, details)

            uri = sub_details['uri']

            def on_event(*args, **kwargs):
                details = kwargs.pop('details')
                self.publish(uri, *args, **kwargs)

            yield other_session.subscribe(on_event, uri)

        yield self.subscribe(on_subscription_create, u"wamp.subscription.on_create", options=SubscribeOptions(details_arg="details"))

        print("CoreBridge: EdgeBridge established")


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
