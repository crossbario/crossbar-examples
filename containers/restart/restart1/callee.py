import os
import threading

import txaio
txaio.use_twisted()
from txaio import make_logger

from twisted.internet.defer import inlineCallbacks

from autobahn.wamp.types import CallDetails, RegisterOptions
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError
from autobahn import wamp


class MyCallee(ApplicationSession):

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

        yield self.register(self, options=RegisterOptions(invoke='roundrobin'))

    @wamp.register('com.example.echo')
    def echo(self, data, shorten_by=None, details=None):
        assert details is None or isinstance(details, CallDetails)

        if type(data) != bytes:
            raise ApplicationError(ApplicationError.INVALID_PAYLOAD, '"data" must be bytes, but was {}'.format(type(data)))

        res = (data + data)

        if shorten_by:
            res = res[:-shorten_by]

        self.log.info('{klass}[{ident}].echo(): echo return {reslen} bytes',
                      klass=self.__class__.__name__, ident=self.ident, reslen=len(res))

        return res
