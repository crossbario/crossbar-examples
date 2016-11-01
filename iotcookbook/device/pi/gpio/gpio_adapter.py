import sys
import argparse

import RPi.GPIO as GPIO

import six
import txaio
txaio.use_twisted()

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.task import LoopingCall
from twisted.internet.error import ReactorNotRunning

from autobahn import wamp
from autobahn.wamp.exception import ApplicationError
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner
from autobahn.twisted.choosereactor import install_reactor


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


class GpioAdapter(ApplicationSession):
    """
    Connects the Pi's GPIOs to WAMP.
    """
    PINMODES = {
        'bcm': GPIO.BCM,
        'board': GPIO.BOARD
    }

    @inlineCallbacks
    def onJoin(self, details):

        self._serial = get_serial()
        self._prefix = u'io.crossbar.demo.iotstarterkit.{}.gpio'.format(self._serial)

        self.log.info("Crossbar.io IoT Starterkit Serial No.: {serial}", serial=self._serial)
        self.log.info("GpioAdapter connected: {details}", details=details)

        # get custom configuration
        extra = self.config.extra

        # Device ID and auxiliary info
        self._digout_pins = extra.get("digout_pins", [])
        self._digin_pins = extra.get("digin_pins", [])
        self._scan_rate = extra.get("scan_rate", 30)

        # init GPIO
        GPIO.setwarnings(False)
        pinmode = extra.get("pin_mode", "bcm")
        if pinmode in GpioAdapter.PINMODES:
            GPIO.setmode(GpioAdapter.PINMODES[pinmode])
        else:
            GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()

        # setup GPIO pins
        for digout_pin in self._digout_pins:
            GPIO.setup(digout_pin, GPIO.OUT)
        for digin_pin in self._digin_pins:
            GPIO.setup(digin_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # setup pin state vectors
        self._digout_state = [False for digout in self._digout_pins]
        self._digin_state = [GPIO.input(digin_pin) == 1 for digin_pin in self._digin_pins]

        # register methods on this object for remote calling via WAMP
        for proc in [self.get_version,
                     self.set_digout,
                     self.get_digout,
                     self.trigger_digout,
                     self.toggle_digout,
                     self.get_digin]:
            uri = u'{}.{}'.format(self._prefix, proc.__name__)
            yield self.register(proc, uri)
            self.log.info("GpioAdapter registered procedure {}".format(uri))

        # start digin scanner
        self._digin_scanner = LoopingCall(self._scan_digins)
        self._digin_scanner.start(1./float(self._scan_rate))

        # signal we are done with initializing our component
        self.publish(u'{}.on_ready'.format(self._prefix))

        # install a heartbeat logger
        self._tick_no = 0
        self._tick_loop = LoopingCall(self._tick)
        self._tick_loop.start(5)

        self.log.info("GpioAdapter ready.")

    def onLeave(self, details):
        self.log.info("Session closed: {details}", details=details)
        self.disconnect()

    def onDisconnect(self):
        self.log.info("Connection closed")
        if self._tick_loop:
            self._tick_loop.stop()
            self._tick_loop = None
        try:
            reactor.stop()
        except ReactorNotRunning:
            pass

    def _tick(self):
        self._tick_no += 1
        self.log.info('I am alive [tick {}]'.format(self._tick_no))

    def get_version(self):
        """
        Get Pi and board version information.
        """
        version = {
            'pi': GPIO.RPI_INFO,
            'board': GPIO.RPI_INFO['P1_REVISION']
        }
        return version

    def _check_digout_arg(self, digout):
        if digout not in range(0, len(self._digout_pins)):
            raise ApplicationError(ApplicationError.INVALID_ARGUMENT, "invalid value '{}' for digout".format(digout))

    def set_digout(self, digout, state):
        """
        Set a digout state.
        """
        self._check_digout_arg(digout)

        if type(state) != bool:
            raise ApplicationError("ApplicationError.INVALID_ARGUMENT", "state must be a bool")

        # only process if state acually changes
        if self._digout_state[digout] != state:
            self._digout_state[digout] = state

            # now set the digout value
            GPIO.output(self._digout_pins[digout], GPIO.HIGH if state else GPIO.LOW)

            # publish WAMP event
            self.publish(u'{}.on_digout_changed'.format(self._prefix), digout=digout, state=state)

            if state:
                self.log.info("digout {} asserted".format(digout))
            else:
                self.log.info("digout {} deasserted".format(digout))

            return True
        else:
            return False

    def get_digout(self, digout=None):
        """
        Get a digout state.
        """
        if digout is not None:
            self._check_digout_arg(digout)
            return self._digout_state[digout]
        else:
            return self._digout_state

    def trigger_digout(self, digout, period=500):
        """
        Trigger a digout.
        """
        self._check_digout_arg(digout)
        self.set_digout(digout, True)
        def clear():
            self.set_digout(digout, False)

        reactor.callLater(float(period)/1000., clear)

    def toggle_digout(self, digout):
        """
        Toggle a digout.
        """
        self._check_digout_arg(digout)
        self.set_digout(digout, not self._digout_state[digout])
        return self._digout_state[digout]

    def _check_digin_arg(self, digin):
        if digin not in range(0, len(self._digin_pins)):
            raise ApplicationError(u"com.example.invalid_argument", "No digin with ID {}".format(digin))

    def get_digin(self, digin = None):
        """
        Get a digin state.
        """
        if digin is not None:
            self._check_digin_arg(digin)
            return self._digin_state[digin]
        else:
            return self._digin_state

    def _scan_digins(self):
        for digin in range(0, len(self._digin_pins)):

            # read value from digin
            state = GPIO.input(self._digin_pins[digin]) == 1

            # only process if state has changed
            if self._digin_state[digin] != state:
                self._digin_state[digin] = state

                # publish WAMP event
                self.publish(u'{}.on_digin_changed'.format(self._prefix), digin=digin, state=state)

                if state:
                    self.log.info("digin {} state asserted".format(digin))
                else:
                    self.log.info("digin {} state unasserted".format(digin))


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

        # these Pins are wired to digouts
        "digout_pins": [13, 19, 5, 6],

        # these Pins are wired to digins
        "digin_pins": [20, 21],

        # we will scan the digins at this rate (Hz)
        "scan_rate": 50
    }

    # create and start app runner for our app component ..
    runner = ApplicationRunner(url=args.router, realm=args.realm, extra=extra)
    runner.run(GpioAdapter, auto_reconnect=True)
