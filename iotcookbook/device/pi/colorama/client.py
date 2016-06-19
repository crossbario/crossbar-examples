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

from neopixel import *


def get_serial():
    with open('/proc/cpuinfo') as fd:
        for line in fd.read().splitlines():
            if line.startswith('Serial'):
                _, serial = line.split(':')
                return u''.format(int(serial.strip()))


class ColoramaDisplay(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info("Session joined: {details}", details=details)

        self._serial = get_serial()

        cfg = self.config.extra

        self._leds = Adafruit_NeoPixel(
            cfg['led_count'],
            cfg['led_pin'],
            cfg['led_freq_hz'],
            cfg['led_dma'],
            cfg['led_invert'],
            cfg['led_brightness'])
        self._leds.begin()
        self.set_uniform_color(0, 0, 0)

        yield self.register(set_uniform_color, u'io.crossbar.iotstarterkit.{}.pixelstrip.set_uniform_color'.format(self._serial))

        self.log.info("ColoramaDisplay ready!")

    def set_uniform_color(self, red, green, blue):
        for i in range(self._leds.numPixels()):
            self._leds.setPixelColor(i, Color(red, green, blue))
        self._leds.show()

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
        u'led_count': 8,            # Number of LED pixels.
        u'led_pin': 12,             # GPIO pin connected to the pixels (must support PWM!).
        u'led_freq_hz': 800000,     # LED signal frequency in hertz (usually 800khz)
        u'led_dma': 5,              # DMA channel to use for generating signal (try 5)
        u'led_brightness': 80,      # Set to 0 for darkest and 255 for brightest
        u'led_invert': False,       # True to invert the signal (when using NPN transistor level shift)
    }

    runner = ApplicationRunner(url=args.router, realm=args.realm, extra=extra)
    runner.run(ColoramaDisplay)
