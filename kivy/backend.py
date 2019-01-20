from __future__ import print_function

import txaio
txaio.use_twisted()

import os
import argparse
import six
import txaio
import random
import sys

from twisted.internet import reactor
from twisted.internet.error import ReactorNotRunning
from twisted.internet.defer import inlineCallbacks, DeferredList

from autobahn.twisted.util import sleep
from autobahn.wamp.types import RegisterOptions, PublishOptions, ComponentConfig
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.exception import ApplicationError


def add2(a, b):
    print('add2 called: {} {}'.format(a, b))
    return a + b


class ClientSession(ApplicationSession):

    def __init__(self, config):
        ApplicationSession.__init__(self, config)
        self._countdown = 5

    def onConnect(self):
        self.log.info('transport connected')

        # lets join a realm .. normally, we would also specify
        # how we would like to authenticate here
        self.join(self.config.realm)

    def onChallenge(self, challenge):
        self.log.info('authentication challenge received')

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info('session joined: {}'.format(details))

        yield self.register(add2, u'com.example.add2')

        for i in range(10):
            res = yield self.call(u'com.example.add2', 23, i * self._countdown)
            self.log.info('result: {}'.format(res))

        i = 0
        while True:
            msg = 'Hello, world! [{}]'.format(i)
            yield self.publish(u'com.example.topic1', msg, options=PublishOptions(acknowledge=True))
            self.log.info(msg)
            yield sleep(1)
            i += 1

    def onLeave(self, details):
        self.log.info('session left: {}'.format(details))
        self.disconnect()

    def onDisconnect(self):
        self.log.info('transport disconnected')
        # this is to clean up stuff. it is not our business to
        # possibly reconnect the underlying connection
        self._countdown -= 1
        if self._countdown <= 0:
            try:
                reactor.stop()
            except ReactorNotRunning:
                pass


if __name__ == '__main__':

    # Crossbar.io connection configuration
    url = u'ws://localhost:8080/ws'
    realm = u'realm1'

    # parse command line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', default=False, help='Enable debug output.')
    parser.add_argument('--url', dest='url', type=six.text_type, default=url, help='The router URL (default: "ws://localhost:8080/ws").')
    parser.add_argument('--realm', dest='realm', type=six.text_type, default=realm, help='The realm to join (default: "realm1").')
    parser.add_argument('--service', dest='service', type=six.text_type, default=u'unknown', help='The service name.')

    args = parser.parse_args()

    # start logging
    if args.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    # any extra info we want to forward to our ClientSession (in self.config.extra)
    extra = {
        u'authextra': {
            u'service': args.service
        }
    }

    print('using python executable {}'.format(sys.executable))
    print('connecting to {}@{}'.format(realm, url))

    # now actually run a WAMP client using our session class ClientSession
    runner = ApplicationRunner(url=args.url, realm=args.realm, extra=extra)
    runner.run(ClientSession, auto_reconnect=True)
