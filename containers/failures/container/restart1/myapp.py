import os
from pprint import pformat

import txaio
txaio.use_twisted()
from txaio import make_logger

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.util import sleep
from autobahn.wamp.types import CallDetails, RegisterOptions
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError
from autobahn import wamp


class MySession(ApplicationSession):

    log = make_logger()

    def __init__(self, config):
        self.log.info('MySession.__init__(config={config})', config=str(config))
        ApplicationSession.__init__(self, config)

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info('MySession.onJoin(details={details})', details=details)

        yield self.register(self, options=RegisterOptions(invoke='roundrobin'))

        n = 2
        running = True
        while running:
            data = os.urandom(n + 1)
            try:
                res = yield self.call('com.example.echo', data)
            except:
                self.log.failure()
                running = False
            else:
                self.log.info('call succeeded with result data length {}'.format(n))
                n = n * 2
                yield sleep(1)

        yield self.leave()

    @wamp.register('com.example.echo')
    def echo(self, data, shorten_by=None, details=None):
        assert details is None or isinstance(details, CallDetails)

        if type(data) != bytes:
            raise ApplicationError(ApplicationError.INVALID_PAYLOAD, '"data" must be bytes, but was {}'.format(type(data)))

        res = (data + data)

        if shorten_by:
            res = res[:-shorten_by]

        self.log.info('{klass}.echo(): echo return {reslen} bytes',
                      klass=self.__class__.__name__, reslen=len(res))

        return res
