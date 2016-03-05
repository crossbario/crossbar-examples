import argparse

import six
import txaio
txaio.use_twisted()

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.error import ReactorNotRunning

from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner

from Adafruit_QuadAlphanum import QuadAlphanum


class VotesListener(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info("Session joined: {details}", details=details)

        self._disp = QuadAlphanum(0x70, 1)
        self._disp.clear()
        self._disp.setBrightness(15)

        def onvote(vote):
            if vote[u'subject'] == u'Banana':
                text = "{:0>4d}".format(votes[u'votes'])
                self._disp.setMessage(text)

        yield self.subscribe(onvote, u'io.crossbar.demo.vote.onvote')

        self.log.info("Votes listener ready!")

    def onLeave(self, details):
        self.log.info("Session closed: {details}", details=details)
        self.disconnect()

    def onDisconnect(self):
        self.log.info("Connection closed")
        self._disp.clear()
        try:
            reactor.stop()
        except ReactorNotRunning:
            pass


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output.')
    parser.add_argument("--router", type=six.text_type, default=u"wss://demo.crossbar.io/ws", help='WAMP router URL.')
    parser.add_argument("--realm", type=six.text_type, default=u"crossbardemo", help='WAMP router realm.')

    args = parser.parse_args()

    if args.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    extra = {
    }

    runner = ApplicationRunner(url=args.router, realm=args.realm, extra=extra)
    runner.run(VotesListener)
