##############################################################################
##
##                    Crossbar.io Smart Replenishment
##     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
##
##############################################################################

import os
import sys
import argparse
import shelve
import time


import RPi.GPIO as GPIO
import Adafruit_ADS1x15

import six
import txaio
txaio.use_twisted()

from twisted.internet import reactor
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue, CancelledError
from twisted.internet.task import LoopingCall
from twisted.internet.error import ReactorNotRunning

from autobahn import wamp
from autobahn.wamp.types import PublishOptions, RegisterOptions
from autobahn.wamp.exception import ApplicationError
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner
from autobahn.twisted.choosereactor import install_reactor
from autobahn.util import utcnow

from autobahn.twisted.util import sleep

import socket
import RPi.GPIO as GPIO


def get_serial():
    """
    Get the Pi's serial number.
    """
    with open('/proc/cpuinfo') as fd:
        for line in fd.read().splitlines():
            line = line.strip()
            if line.startswith('Serial'):
                _, serial = line.split(':')
                return u'{}'.format(int(serial.strip(), 16))


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return s.getsockname()[0]


class WPad(ApplicationSession):
    """
    Connects the Pi's GPIOs to WAMP.
    """
    PINMODES = {
        'bcm': GPIO.BCM,
        'board': GPIO.BOARD
    }

    def _select_row(self, row=None):
        i = 0
        for pin in self._row_pins:
            if row is None or row != i:
                GPIO.output(pin, GPIO.HIGH)
            else:
                GPIO.output(pin, GPIO.LOW)
            i += 1

    def onJoin(self, details):

        extra = self.config.extra

        self._serial = get_serial()
        self._my_ip = get_ip_address()
        self._joined_at = time.strftime("%H:%M")

        self._app_prefix = u'io.crossbar.demo.wpad'
        self._prefix = u'{}.wpad.{}'.format(self._app_prefix, self._serial)

        self.log.info("Crossbar.io IoT Starterkit Serial No.: {serial}", serial=self._serial)
        self.log.info("WPad connected: {details}", details=details)

        # setup GPIO
        GPIO.setwarnings(False)
        pinmode = extra.get("pin_mode", "bcm")
        if pinmode in WPad.PINMODES:
            GPIO.setmode(WPad.PINMODES[pinmode])
        else:
            GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()

        self._row_pins = extra.get("row_pins", [])
        for pin in self._row_pins:
            GPIO.setup(pin, GPIO.OUT)
        self._select_row(0)

        # setup ADC
        self._adc = Adafruit_ADS1x15.ADS1015()

        def log_adc():
            values = []
            for i in range(4):
                values.append(self._adc.read_adc(i, gain=8))
            nvalues = [int(round(100. * ((2048. - float(x)) / 2048.))) for x in values]
            print(nvalues)
            self.publish(u'{}.on_wpad'.format(self._prefix), nvalues)

        LoopingCall(log_adc).start(.5)

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

    # parse command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output.')
    parser.add_argument("--router", type=six.text_type, default=u"wss://demo.crossbar.io/ws", help='WAMP router URL.')
    parser.add_argument("--realm", type=six.text_type, default=u"crossbardemo", help='WAMP router realm.')

    args = parser.parse_args()

    if args.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    # custom configuration data
    extra = {
        # PIN numbering mode (use "bcm" or "board")
        "pin_mode": "bcm",

        # these pins are digouts wired to the sensor matrix rows (active GND!)
        "row_pins": [26, 19, 13, 6],
    }

    # create and start app runner for our app component ..
    runner = ApplicationRunner(url=args.router, realm=args.realm, extra=extra)
    runner.run(WPad, auto_reconnect=True)
