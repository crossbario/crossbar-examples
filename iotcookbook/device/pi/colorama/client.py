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
    """
    Get the Pi's serial number.
    """
    with open('/proc/cpuinfo') as fd:
        for line in fd.read().splitlines():
            line = line.strip()
            if line.startswith('Serial'):
                _, serial = line.split(':')
                return u'{}'.format(int(serial.strip(), 16))


class ColoramaDisplay(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        self._serial = get_serial()
        self._prefix = u'io.crossbar.demo.iotstarterkit.{}.pixelstrip'.format(self._serial)

        self.log.info("Crossbar.io IoT Starterkit Serial No.: {serial}", serial=self._serial)
        self.log.info("ColoramaDisplay connected: {details}", details=details)

        # get custom configuration
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
            (self.flash, 'flash'),
            (self.lightshow, 'lightshow'),
            (self.color_wipe, 'color_wipe'),
            (self.theater_chase, 'theater_chase'),
            (self.rainbow, 'rainbow'),
            (self.rainbow_cycle, 'rainbow_cycle'),
            (self.theater_chaserainbow, 'theater_chaserainbow'),

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

    @inlineCallbacks
    def lightshow(self):
        # Color wipe animations.
        yield self.color_wipe(255, 0, 0)  # Red wipe
        yield self.color_wipe(0, 255, 0)  # Blue wipe
        yield self.color_wipe(0, 0, 255)  # Green wipe
        # Theater chase animations.
        yield self.theater_chase(127, 127, 127)  # White theater chase
        yield self.theater_chase(127,   0,   0)  # Red theater chase
        yield self.theater_chase(0,   0, 127)  # Blue theater chase
        # Rainbow animations.
        yield self.rainbow()
        yield self.rainbow_cycle()
        #yield self.theater_chase_rainbow()
        yield self.flash()

    # Define functions which animate LEDs in various ways.
    @inlineCallbacks
    def color_wipe(self, r, g, b, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self._leds.numPixels()):
            self.set_color(r, g, b, i)
            yield sleep(wait_ms / 1000.0)

    @inlineCallbacks
    def theater_chase(self, r, g, b, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self._leds.numPixels(), 3):
                    self.set_color(r, g, b, i + q)
                yield sleep(wait_ms / 1000.0)
                for i in range(0, self._leds.numPixels(), 3):
                    self.set_color(0, 0, 0, i + q)

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3)

    @inlineCallbacks
    def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256 * iterations):
            for i in range(self._leds.numPixels()):
                r, g, b = self.wheel((i + j) & 255)
                self.set_color(r, g, b, i)
            yield sleep(wait_ms / 1000.0)

    @inlineCallbacks
    def rainbow_cycle(self, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256 * iterations):
            for i in range(self._leds.numPixels()):
                r, g, b = self.wheel(((i * 256 / self._leds.numPixels()) + j) & 255)
                self.set_color(r, g, b, i)
            yield sleep(wait_ms / 1000.0)

    @inlineCallbacks
    def theater_chaserainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self._leds.numPixels(), 3):
                    r, g, b = self.wheel((i+j) % 255)
                    self.set_color(r, g, b, i + q)
                yield sleep(wait_ms / 1000.0)
                for i in range(0, self._leds.numPixels(), 3):
                    self.set_color(0, 0, 0, i)

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

    # parse command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output.')
    parser.add_argument("--router", type=six.text_type, default=u"wss://demo.crossbar.io/ws", help='WAMP router URL.')
    parser.add_argument("--realm", type=six.text_type, default=u"crossbardemo", help='WAMP router realm.')

    args = parser.parse_args()

    # custom configuration data
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

    # create and start app runner for our app component ..
    runner = ApplicationRunner(url=args.router, realm=args.realm, extra=extra)
    runner.run(ColoramaDisplay, auto_reconnect=True)
