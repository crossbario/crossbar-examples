from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError
from autobahn.wamp.types import SubscribeOptions, RegisterOptions


class AppSession(ApplicationSession):

    log = Logger()

    _this_service = u'service1'
    _other_services = [u'service2', u'service3']

    @inlineCallbacks
    def onJoin(self, details):

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
