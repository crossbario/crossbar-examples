import os
import threading

import txaio
txaio.use_twisted()
from txaio import make_logger

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.util import sleep
from autobahn.wamp.types import CallDetails, RegisterOptions
from autobahn.twisted.wamp import ApplicationSession
from autobahn import wamp


class MyCallerCallee(ApplicationSession):

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

        n = 2
        running = True
        while running and n <= 2**25:
            data = os.urandom(n)
            try:
                res = yield self.call('com.example.echo', data, shorten_by=0)
            except:
                self.log.failure()
                running = False
            else:
                self.log.info('{klass}[{ident}].call(): succeeded for n={n} with result data length {reslen}',
                              klass=self.__class__.__name__, ident=self.ident, n=n, reslen=len(res))
                n = n * 2
                yield sleep(1)

        self.log.info('Encountered error at n={n}', n=n)

        yield sleep(1)

        yield self.call('com.example.echo', os.urandom(16))

        self.log.info('Ok, session still working - leaving now ..')

        yield self.leave()

    @wamp.register('com.example.echo')
    def echo(self, data, shorten_by=None, details=None):
        assert type(data) == bytes, '"data" must be bytes, but was {}'.format(type(data))
        assert shorten_by is None or type(shorten_by) == int, '"shorten_by" must be int, but was {}'.format(type(shorten_by))
        assert details is None or isinstance(details, CallDetails), '"details" must be CallDetails, but was {}'.format(type(details))

        res = (data + data)
        if shorten_by:
            res = res[:-shorten_by]

        self.log.info('{klass}[{ident}].echo(data={dlen}, shorten_by={shorten_by}, details={details}): echo return {reslen} bytes',
                      klass=self.__class__.__name__,
                      ident=self.ident,
                      shorten_by=shorten_by,
                      details=details,
                      dlen=len(data),
                      reslen=len(res))

        return res
