import os
import argparse
import six
import txaio
txaio.use_twisted()

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.error import ReactorNotRunning
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

from autobahn.twisted.util import sleep
from autobahn.wamp.exception import ApplicationError
from autobahn.wamp.types import SubscribeOptions, RegisterOptions


class ClientSession(ApplicationSession):
    log = txaio.make_logger()

    _this_service = u'service1'
    _other_services = [u'service0', u'service2', u'service3']


    def onConnect(self):
        self.log.info("Client connected")
        self.join(self.config.realm, [u'anonymous'])

    def onChallenge(self, challenge):
        self.log.info("Challenge for method {authmethod} received", authmethod=challenge.method)
        raise Exception("We haven't asked for authentication!")

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info("Client session joined {details}", details=details)

        # SUBSCRIBE to a topic and receive events
        #
        def on_counter(msg, details=None):
            self.log.info("AutobahnPython/SUBSCRIBE: event for 'on_counter' received: {msg}, {details}", msg=msg, details=details)

        for svc in self._other_services:
            topic = u'com.example.{}.on_counter'.format(svc)
            sub = yield self.subscribe(on_counter, topic, options=SubscribeOptions(details_arg='details'))
            self.log.info("AutobahnPython/SUBSCRIBE: subscribed to {topic}", topic=topic)

        # REGISTER a procedure for remote calling
        #
        proc = u'com.example.{}.add2'.format(self._this_service)

        def add2(x, y):
            self.log.info("AutobahnPython/REGISTER: {proc} called with {x} and {y}", proc=proc, x=x, y=y)
            return x + y

        reg = yield self.register(add2, proc)
        self.log.info("AutobahnPython/REGISTER: procedure {proc} registered", proc=proc)

        # PUBLISH and CALL every second .. forever
        #
        counter = 0
        while True:
            for svc in self._other_services:

                # PUBLISH an event
                topic = u'com.example.{}.on_counter'.format(svc)
                yield self.publish(topic, counter)
                self.log.info("AutobahnPython/PUBLISH: published to {topic} with counter {counter}",
                              topic=topic, counter=counter)
                counter += 1

                # CALL a remote procedure
                proc = u'com.example.{}.add2'.format(svc)
                try:
                    res = yield self.call(proc, counter, 3)
                    self.log.info("AutobahnPython/CALL: {proc} called with result: {result}",
                                  proc=proc, result=res)
                except ApplicationError as e:
                    ## ignore errors due to the frontend not yet having
                    ## registered the procedure we would like to call
                    if e.error != 'wamp.error.no_such_procedure':
                        raise e

            yield sleep(1)

    def onLeave(self, details):
        self.log.info("Router session closed ({details})", details=details)
        self.disconnect()

    def onDisconnect(self):
        self.log.info("Router connection closed")
        try:
            reactor.stop()
        except ReactorNotRunning:
            pass


if __name__ == '__main__':

    # Crossbar.io connection configuration
    url = os.environ.get('CBURL', u'ws://localhost:8080/ws')
    realm = os.environ.get('CBREALM', u'realm1')

    # parse command line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output.')
    parser.add_argument('--url', dest='url', type=six.text_type, default=url, help='The router URL (default: "ws://localhost:8080/ws").')
    parser.add_argument('--realm', dest='realm', type=six.text_type, default=realm, help='The realm to join (default: "realm1").')

    args = parser.parse_args()

    # start logging
    if args.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    # any extra info we want to forward to our ClientSession (in self.config.extra)
    extra = {
        u'foobar': u'A custom value'
    }

    # now actually run a WAMP client using our session class ClientSession
    runner = ApplicationRunner(url=args.url, realm=args.realm, extra=extra)
    runner.run(ClientSession)
