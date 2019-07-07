import os
import threading

import txaio
txaio.use_twisted()
from txaio import make_logger

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.util import sleep
from autobahn.wamp.types import PublishOptions
from autobahn.twisted.wamp import ApplicationSession


class MyPublisher(ApplicationSession):

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

        n = 2
        running = True
        last_error = None
        while running and n <= 2**25:
            data = os.urandom(n + 1)
            try:
                res = yield self.publish('com.example.topic1', data,
                                         options=PublishOptions(acknowledge=True, exclude_me=False))
            except Exception as e:
                self.log.failure()
                running = False
                last_error = e
            else:
                self.log.info('{klass}[{ident}].publish(): succeeded for n={n}, res={res}',
                              klass=self.__class__.__name__, ident=self.ident, n=n, res=res)
                n = n * 2
                yield sleep(1)

        if last_error:
            self.log.info('Encountered error at n={n}', n=n)
        else:
            self.log.info('Finished (without error) at n={n}', n=n)

        yield sleep(1)

        yield self.publish('com.example.topic1', os.urandom(16), options=PublishOptions(acknowledge=True))

        self.log.info('Ok, session still working - leaving now ..')

        yield self.leave()
