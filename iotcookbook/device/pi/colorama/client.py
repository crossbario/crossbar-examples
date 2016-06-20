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

from neopixel import Adafruit_NeoPixel, Color


def get_serial():
    with open('/proc/cpuinfo') as fd:
        for line in fd.read().splitlines():
            line = line.strip()
            if line.startswith('Serial'):
                _, serial = line.split(':')
                return u'{}'.format(int(serial.strip(), 16))


class ColoramaDisplay(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info("Session joined: {details}", details=details)

        self._serial = get_serial()
        self._prefix = u'io.crossbar.demo.iotstarterkit.{}.pixelstrip'.format(self._serial)

        self.log.info("Crossbar.io IoT Starterkit Serial No.: {serial}", serial=self._serial)

        cfg = self.config.extra

        self._leds = Adafruit_NeoPixel(
            cfg['led_count'],
            cfg['led_pin'],
            cfg['led_freq_hz'],
            cfg['led_dma'],
            cfg['led_invert'],
            cfg['led_brightness'])

        self._leds.begin()

        for proc in [
            (self.set_color, 'set_color'),
            (self.get_color, 'get_color'),
        ]:
            yield self.register(proc[0], u'{}.{}'.format(self._prefix, proc[1]))

        self.flash()

        self.log.info("ColoramaDisplay ready!")

    @inlineCallbacks
    def flash(self, delay=50, repeat=5):
        delay = float(delay) / 1000.
        for i in range(repeat):
            self.set_color(0xe1, 0xda, 0x05)
            yield sleep(2 * delay)
            self.set_color(0x52, 0x42, 0x00)
            yield sleep(delay)

    def set_color(self, red, green, blue, k=None):
        if k is None:
            for i in range(self._leds.numPixels()):
                # FIXME: not sure, but we need to swap this here. maybe it is the specific neopixels?
                self._leds.setPixelColorRGB(i, green, red, blue)
                color_change = {
                    u'led': i,
                    u'r': red,
                    u'g': green,
                    u'b': blue
                }
                self.publish(u'{}.on_color_set'.format(self._prefix), color_change)
        else:
                # FIXME: not sure, but we need to swap this here. maybe it is the specific neopixels?
            self._leds.setPixelColorRGB(k, green, red, blue)
            color_change = {
                u'led': k,
                u'r': red,
                u'g': green,
                u'b': blue
            }
            self.publish(u'{}.on_color_set'.format(self._prefix), color_change)
        self._leds.show()

    def get_color(self, k):
        c = self._leds.getPixelColor(k)
        color = {
            u'g': c >> 16,
            u'r': (c >> 8) & 0xff,
            u'b': c & 0xff,
        }
        return color

    def onLeave(self, details):
        self.log.info("Session closed: {details}", details=details)
        self.disconnect()

    def onDisconnect(self):
        self.log.info("Connection closed")
        for i in range(self._leds.numPixels()):
            self._leds.setPixelColorRGB(i, 0, 0, 0)
        self._leds.show()
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
        u'led_brightness': 96,      # Set to 0 for darkest and 255 for brightest
        u'led_invert': False,       # True to invert the signal (when using NPN transistor level shift)
    }

    runner = ApplicationRunner(url=args.router, realm=args.realm, extra=extra)
    runner.run(ColoramaDisplay)
