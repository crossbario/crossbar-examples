import argparse
import six
import txaio

from twisted.internet import reactor
from twisted.internet.error import ReactorNotRunning
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError
from autobahn.wamp.types import SubscribeOptions, RegisterOptions


class ClientSession(ApplicationSession):

    log = txaio.make_logger()

    def onConnect(self):
        self.log.info("Client connected")
        self.join(self.config.realm, [u'anonymous'])

    def onChallenge(self, challenge):
        self.log.info("Challenge for method {authmethod} received", authmethod=challenge.method)
        raise Exception("We haven't asked for authentication!")

    def onLeave(self, details):
        self.log.info("Router session closed ({details})", details=details)
        self.disconnect()

    def onDisconnect(self):
        self.log.info("Router connection closed")
        try:
            reactor.stop()
        except ReactorNotRunning:
            pass

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info("Client session joined {details}", details=details)

        # SUBSCRIBE to a topic and receive events
        def onhello(msg, details=None):
            self.log.info("event for 'onhello' received: {msg} {details}", msg=msg, details=details)

        yield self.subscribe(onhello, u'com.example.onhello', options=SubscribeOptions(details_arg='details'))
        self.log.info("subscribed to topic 'onhello'")

        # REGISTER a procedure for remote calling
        def add2(x, y, details=None):
            self.log.info("add2() called with {x} and {y} - {details}", x=x, y=y, details=details)
            return x + y

        yield self.register(add2, u'com.example.add2', options=RegisterOptions(details_arg='details'))
        self.log.info("procedure add2() registered")

        # PUBLISH and CALL every second .. forever
        counter = 0
        while True:

            # PUBLISH an event
            yield self.publish(u'com.example.oncounter', counter)
            self.log.info("published to 'oncounter' with counter {counter}",
                          counter=counter)
            counter += 1

            # CALL a remote procedure
            try:
                res = yield self.call(u'com.example.mul2', counter, 3)
                self.log.info("mul2() called with result: {result}",
                              result=res)
            except ApplicationError as e:
                # ignore errors due to the frontend not yet having
                # registered the procedure we would like to call
                if e.error != u'wamp.error.no_such_procedure':
                    raise e

            yield sleep(1)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output.')
    parser.add_argument('--url', dest='url', type=six.text_type, default=u'ws://localhost:8080/ws', help='The router URL (default: "ws://localhost:8080/ws").')
    parser.add_argument('--realm', dest='realm', type=six.text_type, default=u'realm1', help='The realm to join (default: "realm1").')

    args = parser.parse_args()

    if args.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    extra = {
        u'foobar': u'A custom value'
    }

    runner = ApplicationRunner(url=args.url, realm=args.realm, extra=extra)
    runner.run(ClientSession)
