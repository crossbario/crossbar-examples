import os
import threading

import txaio
txaio.use_twisted()
from txaio import make_logger

from twisted.internet.defer import inlineCallbacks

from autobahn.wamp.types import EventDetails, SubscribeOptions
from autobahn.twisted.wamp import ApplicationSession
from autobahn import wamp


class MySubscriber(ApplicationSession):

    log = make_logger()

    def __init__(self, config):
        self.ident = '{}:{}'.format(os.getpid(), threading.get_ident())

        self.log.info('{klass}[{ident}].__init__(config={config})',
                      klass=self.__class__.__name__, ident=self.ident, config=str(config))

        ApplicationSession.__init__(self, config)

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info('{klass}[{ident}].onJoin(details={details})',
                      klass=self.__class__.__name__, ident=self.ident, details=details)

        yield self.subscribe(self, options=SubscribeOptions(details=True))

    @wamp.subscribe('com.example.topic1')
    def on_topic1(self, data, details=None):
        assert type(data) == bytes, '"data" must be bytes, but was {}'.format(type(data))
        assert details is None or isinstance(details, EventDetails), '"details" must be EventDetails, but was {}'.format(type(details))

        self.log.info('{klass}[{ident}].on_topic1(data={dlen}, details={details})',
                      klass=self.__class__.__name__,
                      ident=self.ident,
                      details=details,
                      dlen=len(data))
