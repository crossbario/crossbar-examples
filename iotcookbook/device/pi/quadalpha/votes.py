import time
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

import socket

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return s.getsockname()[0]

import RPi.GPIO as GPIO
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

        my_ip = get_ip_address()
        joined_at = time.strftime("%H:%M")

        # the voting subject we will display and vote for
        subject = self.config.extra[u'subject']

        # our quad, alphanumeric display: https://www.adafruit.com/products/2157
        self._disp = QuadAlphanum(self.config.extra[u'i2c_address'])
        self._disp.clear()
        self._disp.setBrightness(int(round(self.config.extra[u'brightness'] * 15)))

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
            yield scrollText(self._disp, "ip={} joined={} subject={} ...".format(my_ip, joined_at, subject).upper())

            # get the current votes
            votes = yield self.call(u'io.crossbar.demo.vote.get')
            for vote in votes:
                if vote[u'subject'] == subject:
                    setVotes(vote[u'votes'])

        # every couple of secs, display a notice
        LoopingCall(displayNotice).start(60)


        # init GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()
        GPIO.setup(self.config.extra[u'button_pin'], GPIO.IN)

        self._button_state = False

        @inlineCallbacks
        def scan_buttons():
            new_state = GPIO.input(self.config.extra[u'button_pin']) == 1
            if new_state != self._button_state:
                self.log.info("Button state change: {new_state}", new_state=new_state)
                if new_state:
                    yield self.call(u'io.crossbar.demo.vote.vote', subject)
                self._button_state = new_state

        # periodically scan buttons
        scanner = LoopingCall(scan_buttons)
        scanner.start(1./50.)


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

    # parse command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output.')
    parser.add_argument("--router", type=six.text_type, default=u"wss://demo.crossbar.io/ws", help='WAMP router URL.')
    parser.add_argument("--realm", type=six.text_type, default=u"crossbardemo", help='WAMP router realm.')
    parser.add_argument("--id", type=unicode, default=None, help='The Device ID to use. Default is to use the RaspberryPi Serial Number')

    args = parser.parse_args()

    if args.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    # custom configuration data
    extra = {
        # the voting subject the display will show, and the button
        # will trigger voting for
        u'subject': u'Banana',

        # the button configuration (a BCM digital pin number is required,
        # see here https://pinout.xyz/)
        u'button_pin': 26,

        # the quad-alpha display hardware configuration
        u'i2c_address': 0x77,
        u'brightness': 1.,
    }

    # create and start app runner for our app component ..
    runner = ApplicationRunner(url=args.router, realm=args.realm, extra=extra)
    runner.run(VotesListener, auto_reconnect=True)
