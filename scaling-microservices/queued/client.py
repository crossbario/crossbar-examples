import argparse
import time

import six

import txaio
txaio.use_twisted()

from twisted.internet import reactor
from twisted.internet.error import ReactorNotRunning
from twisted.internet.defer import inlineCallbacks

from autobahn.wamp.types import ComponentConfig
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.twisted.util import sleep
from autobahn.wamp.exception import ApplicationError

class ComputeClient(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info('session joined: {}'.format(details))

        calls = []

        started = time.time()

        for i in range(20):
            self.log.info('issueing call {i} ..', i=i)
            d = self.call(u'com.example.compute', i, 2)
            calls.append(d)

        results = yield txaio.gather(calls)

        ended = time.time()
        runtime = ended - started

        self.log.info('total run-time (wallclock): {runtime}', runtime=runtime)
        for result in results:
            if result:
                self.log.info('{result}', result=result)

        yield self.leave()

    def onLeave(self, details):
        self.log.info('session left: {}'.format(details))
        self.disconnect()

    def onDisconnect(self):
        self.log.info('transport disconnected')
        try:
            reactor.stop()
        except ReactorNotRunning:
            pass


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output.')
    parser.add_argument('--router', type=six.text_type, default=u'ws://127.0.0.1:8080/ws', help='WAMP router URL.')
    parser.add_argument('--realm', type=six.text_type, default=u'realm1', help='WAMP router realm.')

    args = parser.parse_args()

    if args.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    config = ComponentConfig(args.realm, extra={})

    session = ComputeClient(config)

    runner = ApplicationRunner(args.router, args.realm)

    runner.run(session, auto_reconnect=True)
