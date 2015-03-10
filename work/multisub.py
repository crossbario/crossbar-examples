from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.wamp.types import PublishOptions, SubscribeOptions
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner
from autobahn.twisted.util import sleep


class MyComponent(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        print("session ready")

        self.received = []

        topic1 = u"com.example.topic1"
        sub_options = SubscribeOptions(details_arg="details")
        pub_options = PublishOptions(acknowledge=True, exclude_me=False)
        delay = 0.1

        # subscribe handler1 on topic
        #
        def handler1(value, details=None):
            print("handler1 got event")
            self.received.append(("handler1", value, details.publication))

        sub1 = yield self.subscribe(handler1, topic1, options=sub_options)
        print("handler1 subscribed: {}".format(sub1), sub1)

        res = yield self.publish(topic1, 1, options=pub_options)
        print("event 1 published: {}".format(res))
        yield sleep(delay)

        # subscribe handler2 on same topic
        #
        def handler2(value, details=None):
            print("handler2 got event")
            self.received.append(("handler2", value, details.publication))

        sub2 = yield self.subscribe(handler2, topic1, options=sub_options)
        print("handler2 subscribed: {}".format(sub2), sub2)

        res = yield self.publish(topic1, 2, options=pub_options)
        print("event 2 published: {}".format(res))
        yield sleep(delay)

        # subscribe handler2 on same topic a second time
        #
        sub2b = yield self.subscribe(handler2, topic1, options=sub_options)
        print("handler2 subscribed 2nd: {}".format(sub2b), sub2b)

        res = yield self.publish(topic1, 3, options=pub_options)
        print("event 3 published: {}".format(res))
        yield sleep(delay)

        # unsubscribe subscription1
        #
        yield sub1.unsubscribe()
        print("handler1 unsubscribed: {}".format(sub1), sub1)

        res = yield self.publish(topic1, 4, options=pub_options)
        print("event 4 published: {}".format(res))
        yield sleep(delay)

        # unsubscribe subscription2
        #
        yield sub2.unsubscribe()
        print("handler2 unsubscribed: {}".format(sub2), sub2)

        res = yield self.publish(topic1, 5, options=pub_options)
        print("event 5 published: {}".format(res))
        yield sleep(delay)

        # unsubscribe subscription2b
        #
        yield sub2b.unsubscribe()
        print("handler2 unsubscribed 2nd: {}".format(sub2b), sub2b)

        res = yield self.publish(topic1, 6, options=pub_options)
        print("event 6 published: {}".format(res))
        yield sleep(delay)

        print("Done!", self.received)
        self.leave()

    def onLeave(self, details):
        print("session left")
        self.disconnect()

    def onDisconnect(self):
        print("transport disconnected")
        reactor.stop()


if __name__ == '__main__':
    runner = ApplicationRunner(url=u"ws://localhost:8080/ws", realm=u"realm1",
        debug=False, debug_wamp=False)
    runner.run(MyComponent)
