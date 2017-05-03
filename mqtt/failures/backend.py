from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.util import sleep
from autobahn.wamp.types import SubscribeOptions, PublishOptions


class Backend(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        self.log.info('backend joined: {details}', details=details)

        def on_event(msg, details=None):
            self.log.info('received event on {topic}: {msg}', topic=details.topic, msg=msg)
            self.log.info('details: {details}', details=details)

        sub = yield self.subscribe(on_event, u'', SubscribeOptions(match=u'prefix', details=True))

        self.log.info('backend subscribed: {sub}', sub=sub)

        counter = 0

        while True:
            msg = u'counter is at {}'.format(counter)
            pub = yield self.publish(u'topic1', msg, options=PublishOptions(exclude_me=False, acknowledge=True))
            self.log.info('event published: {pub}', pub=pub)
            counter += 1
            yield sleep(1)
