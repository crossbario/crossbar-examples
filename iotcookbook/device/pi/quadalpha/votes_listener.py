import argparse

import six
import txaio
txaio.use_twisted()

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.error import ReactorNotRunning
from twisted.internet.task import LoopingCall

from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner
from autobahn.twisted.util import sleep

from Adafruit_QuadAlphanum import QuadAlphanum


@inlineCallbacks
def scrollText(disp, text):
    s = text + "    "
    for i in range(len(s)):
        disp.setMessage(s[i:i+4])
        yield sleep(.2)


class VotesListener(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info("Session joined: {details}", details=details)

        # our quad, alphanumeric display: https://www.adafruit.com/products/2157
        self._disp = QuadAlphanum(self.config.extra[u'i2c_address'])
        self._disp.clear()
        self._disp.setBrightness(int(round(self.config.extra[u'brightness'] * 15)))

        # the voting subject we will display
        subject = self.config.extra[u'subject']

        # display votes for subject on display
        def setVotes(votes):
            if votes < 10000:
                text = "{:0>4d}".format(votes)
            else:
                text = "MANY"
            self._disp.setMessage(text)

        # get notified of new votes
        def onVote(vote):
            if vote[u'subject'] == subject:
                setVotes(vote[u'votes'])

        yield self.subscribe(onVote, u'io.crossbar.demo.vote.onvote')

        # get notified of votes being reset
        @inlineCallbacks
        def onReset():
            self._disp.setMessage('****')
            yield sleep(.1)
            setVotes(0)

        yield self.subscribe(onReset, u'io.crossbar.demo.vote.onreset')

        @inlineCallbacks
        def displayNotice():
            yield scrollText(self._disp, "listening on {} votes".format(subject).upper())

            # get the current votes
            votes = yield self.call(u'io.crossbar.demo.vote.get')
            for vote in votes:
                if vote[u'subject'] == subject:
                    setVotes(vote[u'votes'])

        #yield displayNotice()
        LoopingCall(displayNotice).start(4)

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
        u'i2c_address': 0x70,
        u'brightness': 1.,
        u'subject': u'Banana'
    }

    runner = ApplicationRunner(url=args.router, realm=args.realm, extra=extra)
    runner.run(VotesListener)
