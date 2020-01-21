import os
import time
import argparse
import random

import six
import txaio
txaio.use_twisted()

import netifaces

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.error import ReactorNotRunning
from twisted.internet.task import LoopingCall

from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner
from autobahn.twisted.util import sleep

from hexdisplay import HexDisplay


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


class HexDisplayComponent(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        self._serial = get_serial()
        self._prefix = 'io.crossbar.demo.iotstarterkit.{}.hexdisplay'.format(self._serial)

        self.log.info("Crossbar.io IoT Starterkit Serial No.: {serial}", serial=self._serial)
        self.log.info("HexDisplayComponent connected: {details}", details=details)

        # get custom configuration
        cfg = self.config.extra

        # initialize display
        self._display = HexDisplay(address=cfg['i2c_address'])
        self._display.begin()
        self._display.set_clear()
        self._display.set_brightness(int(round(cfg['brightness'] * 15)))

        self.log.info("HexDisplayComponent ready!")

        while True:
            yield self.welcome()

    @inlineCallbacks
    def welcome(self):
        msgs = []

        # Pi serial number
        msg = 'serial {:0>6d}'.format(self._serial)
        self.log.info(msg)
        msgs.append(msg)

        # interface IP addresses
        for ifc in netifaces.interfaces():
            if ifc.startswith('wlan') or ifc.startswith('eth'):
                ip4 = '0.0.0.0'
                if netifaces.AF_INET in netifaces.ifaddresses(ifc):
                    ip4_ifcs = netifaces.ifaddresses(ifc)[netifaces.AF_INET]
                    if ip4_ifcs:
                        ip4 = ip4_ifcs[0]['addr']
                msg = 'interface {} {}'.format(ifc, ip4)
                msgs.append(msg)
                self.log.info(msg)

        # scroll informational message
        msg = '     '.join(msgs)
        yield self._display.scroll_message(msg)

        # write the ZOLLHOF logo
        self._display.set_raw_digit(0, 0b0001001)
        self._display.set_raw_digit(1, 0b0111111)
        self._display.set_raw_digit(2, 0b0110110)
        self._display.set_raw_digit(3, 0b1110000)
        self._display.set_raw_digit(4, 0b0111111)
        self._display.set_raw_digit(5, 0b1110001)
        self._display.write_display()

        yield sleep(5)

    def onLeave(self, details):
        self.log.info("Session closed: {details}", details=details)
        self.disconnect()

    def onDisconnect(self):
        self.log.info("Connection closed")
        self._display.set_clear()
        try:
            reactor.stop()
        except ReactorNotRunning:
            pass


if __name__ == '__main__':

    # Crossbar.io connection configuration
    url = os.environ.get('CBURL', 'wss://demo.crossbar.io/ws')
    realm = os.environ.get('CBREALM', 'crossbardemo')

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
        # I2C address of display (check with "sudo i2cdetect -y 1")
        'i2c_address': 0x77,

        # brightness of display (0-1)
        'brightness': 0.6,
    }

    # create and start app runner for our app component ..
    runner = ApplicationRunner(url=args.url, realm=args.realm, extra=extra)
    runner.run(HexDisplayComponent, auto_reconnect=True)
