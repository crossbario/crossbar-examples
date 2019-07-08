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
        last_error = None
        while running and n < 2**20:
            data = os.urandom(n)
            try:
                res = yield self.call('com.example.echo', data)
            except Exception as e:
                self.log.failure()
                last_error = e
                running = False
            else:
                self.log.info('{klass}[{ident}].call(): succeeded for n={n} with result data length {reslen}',
                              klass=self.__class__.__name__, ident=self.ident, n=n, reslen=len(res))
                n = n * 2
                yield sleep(1)

        if last_error:
            self.log.info('Encountered error at n={n}', n=n)
        else:
            self.log.info('Finished (without error) at n={n}', n=n)

        yield sleep(1)

        yield self.call('com.example.echo', os.urandom(16))

        self.log.info('Ok, session still working - leaving now ..')

        yield self.leave()

    @wamp.register('com.example.echo')
    def echo(self, data, details=None):
        assert type(data) == bytes, '"data" must be bytes, but was {}'.format(type(data))
        assert details is None or isinstance(details, CallDetails), '"details" must be CallDetails, but was {}'.format(type(details))

        self.log.info('{klass}[{ident}].echo(data={dlen}, details={details}): echo return {dlen} bytes',
                      klass=self.__class__.__name__,
                      ident=self.ident,
                      details=details,
                      dlen=len(data))

        return data
