import os
import argparse

import six

import txaio
txaio.use_twisted()

import RPi.GPIO as GPIO

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.error import ReactorNotRunning

from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner
from autobahn.twisted.util import sleep


def get_serial():
    """
    Get the Pi's serial number.
    """
    with open('/proc/cpuinfo') as fd:
        for line in fd.read().splitlines():
            line = line.strip()
            if line.startswith('Serial'):
                _, serial = line.split(':')
                return int(serial.strip(), 16)


class BuzzerComponent(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        self._serial = get_serial()
        self._prefix = u'io.crossbar.demo.iotstarterkit.{}.buzzer'.format(self._serial)

        self.log.info("Crossbar.io IoT Starterkit Serial No.: {serial}", serial=self._serial)
        self.log.info("BuzzerComponent connected: {details}", details=details)

        # get custom configuration
        cfg = self.config.extra

        # initialize buzzer
        self._buzzer_pin = cfg['buzzer_pin']
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._buzzer_pin, GPIO.OUT)
        GPIO.output(self._buzzer_pin, 0)

        for proc in [
            (self.beep, 'beep'),
            (self.welcome, 'welcome'),
        ]:
            yield self.register(proc[0], u'{}.{}'.format(self._prefix, proc[1]))

        self.log.info("BuzzerComponent ready!")

        self.welcome()

    @inlineCallbacks
    def welcome(self):
        """
        Play annoying beep sequence.
        """
        # sequence of 7 short beeps
        yield self.beep(7)

        # wait 0.5s
        yield sleep(.5)

        # another 3 longer beeps
        yield self.beep(3, on=200, off=200)

    @inlineCallbacks
    def beep(self, count=1, on=30, off=80):
        """
        Trigger beeping sequence.

        :param count: Number of beeps.
        :type count: int

        :param on: ON duration in ms.
        :type on: int

        :param off: OFF duration in ms.
        :type off: int
        """
        for i in range(count):
            GPIO.output(self._buzzer_pin, 1)
            yield sleep(float(on) / 1000.)
            GPIO.output(self._buzzer_pin, 0)
            yield sleep(float(off) / 1000.)

    def onLeave(self, details):
        self.log.info("Session closed: {details}", details=details)
        self.disconnect()

    def onDisconnect(self):
        self.log.info("Connection closed")
        try:
            reactor.stop()
        except ReactorNotRunning:
            pass


if __name__ == '__main__':

    # Crossbar.io connection configuration
    url = os.environ.get('CBURL', u'wss://demo.crossbar.io/ws')
    realm = os.environ.get('CBREALM', u'crossbardemo')

    # parse command line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output.')
    parser.add_argument('--url', dest='url', type=six.text_type, default=url, help='The router URL (default: "ws://localhost:8080/ws").')
    parser.add_argument('--realm', dest='realm', type=six.text_type, default=realm, help='The realm to join (default: "realm1").')

    args = parser.parse_args()

    # custom configuration data
    if args.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    extra = {
        # GPI pin of buzzer
        u'buzzer_pin': 16,
    }

    # create and start app runner for our app component ..
    runner = ApplicationRunner(url=args.url, realm=args.realm, extra=extra)
    runner.run(BuzzerComponent, auto_reconnect=True)
