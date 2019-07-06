import os
import threading

import txaio
txaio.use_twisted()
from txaio import make_logger

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession


class MyCaller(ApplicationSession):

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

        # avoid "proc not yet registered" (slight hack here)
        yield sleep(2)

        n = 2
        running = True
        last_error = None
        while running and n <= 2**25:
            data = os.urandom(n + 1)
            try:
                res = yield self.call('com.example.echo', data)
            except Exception as e:
                self.log.failure()
                running = False
                last_error = e
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
