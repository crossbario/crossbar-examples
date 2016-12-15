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
from collections import deque

import psutil

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
from neopixel import Adafruit_NeoPixel, Color

from Adafruit_QuadAlphanum import QuadAlphanum


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

    def set_color(self, red, green, blue, k=None):
        if k is None:
            for i in range(self._ledstrip.numPixels()):
                self._ledstrip.setPixelColorRGB(i, green, red, blue)
        else:
            self._ledstrip.setPixelColorRGB(k, green, red, blue)
        self._ledstrip.show()

    @inlineCallbacks
    def flash(self, r=255, g=255, b=255, delay=25, repeat=10):
        delay = float(delay) / 1000.
        for i in range(repeat):
            self.set_color(r, g, b)
            yield sleep(2 * delay)
            self.set_color(0, 0, 0)
            yield sleep(delay)

    @inlineCallbacks
    def _tick(self):
        self._tick_no += 1
        now = time.time()
        self._tick_sent[self._tick_no] = now
        try:
            pub = yield self.publish(u'{}.on_alive'.format(self._prefix), self._tick_no, options=PublishOptions(acknowledge=True, exclude_me=False))
        except:
            self.log.failure()
        else:
            self.log.info('TICK sent [tick {}, pub {}]'.format(self._tick_no, pub.id))

    def show_load(self):
        cpu_load = int(round(psutil.cpu_percent(interval=None)))
        mem_load = int(round(psutil.virtual_memory().percent))
        if cpu_load > 99:
            cpu_load = 99
        if mem_load > 99:
            mem_load = 99

        self._cpu_load.popleft()
        self._cpu_load.append(cpu_load)

        if not self._is_scrolling:
            text = "{:0>2d}{:0>2d}".format(mem_load, cpu_load)
            self._disp.setMessage(text)

    @inlineCallbacks
    def scroll_text(self, disp, text):
        if self._is_scrolling:
            return
        self._is_scrolling = True
        s = text + "    "
        for i in range(len(s)):
            disp.setMessage(s[i:i+4])
            yield sleep(.2)
        self._is_scrolling = False

    @inlineCallbacks
    def onJoin(self, details):

        self._tick_sent = {}
        self._is_scrolling = False

        extra = self.config.extra

        self._serial = get_serial()
        self._my_ip = get_ip_address()
        self._joined_at = time.strftime("%H:%M")

        self._app_prefix = u'io.crossbar.demo.wpad'
        self._prefix = u'{}.wpad.{}'.format(self._app_prefix, self._serial)

        self.log.info("Crossbar.io IoT Starterkit Serial No.: {serial}", serial=self._serial)
        self.log.info("WPad connected: {details}", details=details)

        # setup Neopixel LED strip
        self._ledstrip = Adafruit_NeoPixel(
            extra['led_count'],
            extra['led_pin'],
            extra['led_freq_hz'],
            extra['led_dma'],
            extra['led_invert'],
            extra['led_brightness'])

        self._ledstrip.begin()

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
            # read values from ADC
            values = []
            for i in range(4):
                values.append(self._adc.read_adc(i, gain=8))

            # normalize values
            nvalues = [round(100. * ((2048. - float(x)) / 2048.), 3) for x in values]
            nvalues = [nvalues[2], nvalues[3], nvalues[1], nvalues[0]]

            # illuminate neopixel strip
            for i in range(4):
                col = int(round(255. * float(nvalues[i]) / 100.))
                self._ledstrip.setPixelColorRGB(i * 2, col, col, col)
                self._ledstrip.setPixelColorRGB(i * 2 + 1, col, col, col)
            self._ledstrip.show()

            # publish WAMP event
            self.publish(u'{}.on_wpad'.format(self._prefix), nvalues)

        scan_rate = float(extra.get(u'scan_rate', 50))
        self.log.info('Scanning sensors with {} Hz ..'.format(scan_rate))
        LoopingCall(log_adc).start(1. / scan_rate)

        self._cpu_load = deque()
        for i in range(self._ledstrip.numPixels()):
            self._cpu_load.append(0)


        # our quad, alphanumeric display: https://www.adafruit.com/products/2157
        self._disp = QuadAlphanum(extra[u'i2c_address'])
        self._disp.clear()
        self._disp.setBrightness(int(round(extra[u'brightness'] * 15)))

        @inlineCallbacks
        def displayNotice():
            yield self.scroll_text(self._disp, "IP {} ({})    ".format(self._my_ip, self._joined_at).upper())

        # every couple of secs, display a notice
        LoopingCall(displayNotice).start(53)

        def on_tick(tick_no):
            if tick_no in self._tick_sent:
                rtt = 1000. * (time.time() - self._tick_sent[tick_no])
                del self._tick_sent[tick_no]
            else:
                rtt = None
            self.log.info('TICK received [tick {}, rtt {}]'.format(tick_no, rtt))
            self.flash(r=0, g=255, b=0, repeat=1)

        yield self.subscribe(on_tick, u'{}.on_alive'.format(self._prefix))

        self._tick_no = 0
        self._tick_loop = LoopingCall(self._tick)
        self._tick_loop.start(7)

        LoopingCall(self.show_load).start(1)

        # signal we are done with initializing our component
        self.publish(u'{}.on_ready'.format(self._prefix))
        self.log.info("WPad ready.")

        self.flash()

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
    parser.add_argument("--scanrate", type=int, default=50, help="Sensor scan rate in Hz (should be 5-100 Hz)")

    args = parser.parse_args()

    if args.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    print('connecting to {} to realm {} ..'.format(args.router, args.realm))

    # custom configuration data
    extra = {
        # sensor scan rate in Hz
        u'scan_rate': args.scanrate,

        # PIN numbering mode (use "bcm" or "board")
        u'pin_mode': 'bcm',

        # these pins are digouts wired to the sensor matrix rows (active GND!)
        u'row_pins': [26, 19, 13, 6],

        u'led_count': 8,            # Number of LED pixels.
        u'led_pin': 12,             # GPIO pin connected to the pixels (must support PWM!).
        u'led_freq_hz': 800000,     # LED signal frequency in hertz (usually 800khz)
        u'led_dma': 5,              # DMA channel to use for generating signal (try 5)
        u'led_brightness': 96,      # Set to 0 for darkest and 255 for brightest
        u'led_invert': False,       # True to invert the signal (when using NPN transistor level shift)

        # the quad-alpha display hardware configuration
        u'i2c_address': 0x77,
        u'brightness': 1.,
    }

    # create and start app runner for our app component ..
    runner = ApplicationRunner(url=args.router, realm=args.realm, extra=extra)
    runner.run(WPad, auto_reconnect=True)
