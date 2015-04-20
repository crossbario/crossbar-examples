# Copyright (C) Tavendo GmbH. Open-source licensed under the
# MIT License (http://opensource.org/licenses/MIT)

import sys
import argparse

import RPi.GPIO as GPIO

from twisted.python import log
from twisted.internet.defer import inlineCallbacks
from twisted.internet.task import LoopingCall

from autobahn import wamp
from autobahn.wamp.exception import ApplicationError
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner
from autobahn.twisted.choosereactor import install_reactor


class GpioBackend(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        log.msg("GpioBackend connected.")

        extra = self.config.extra
        self._id = extra['id']
        self._led_pins = extra["led_pins"]
        self._button_pins = extra["button_pins"]
        self._scan_rate = extra["scan_rate"]

        # init GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()
        for led_pin in self._led_pins:
            GPIO.setup(led_pin, GPIO.OUT)
        for btn_pin in self._button_pins:
            GPIO.setup(btn_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

        self._led_status = [False for led in self._led_pins]
        self._btn_status = [GPIO.input(btn_pin) == 1 for btn_pin in self._button_pins]

        self._button_scanner = LoopingCall(self._scan_buttons)
        self._button_scanner.start(1./float(self._scan_rate))

        for proc in [self.set_led, self.get_led, self.toggle_led, self.get_button]:
            uri = u'com.example.device.{}.gpio.{}'.format(self._id, proc.__name__)
            yield self.register(proc, uri)
            log.msg("Registered {}".format(uri))

        log.msg("GpioBackend ready.")

    def _check_led_arg(self, led):
        if led not in range(0, len(self._led_pins)):
            raise ApplicationError("com.example.invalid_argument", "No LED with ID {}".format(led))

    def set_led(self, led, status):
        """
        Set an LED status.
        """
        self._check_led_arg(led)

        if type(status) != bool:
            raise ApplicationError("com.example.invalid_argument", "status must be a bool")

        if self._led_status[led] != status:
            self._led_status[led] = status
            GPIO.output(self._led_pins[led], GPIO.HIGH if status else GPIO.LOW)
            self.publish("com.example.device.{}.gpio.on_led_set".format(self._id), led=led, status=status)
            if status:
                log.msg("LED {} turned on".format(led))
            else:
                log.msg("LED {} turned off".format(led))
            return True
        else:
            return False

    def get_led(self, led = None):
        """
        Get an LED status.
        """
        if led is not None:
            self._check_led_arg(led)
            return self._led_status[led]
        else:
            return self._led_status

    def toggle_led(self, led):
        self._check_led_arg(led)
        self.set_led(led, not self._led_status[led])
        return self._led_status[led]

    def _check_button_arg(self, button):
        if button not in range(0, len(self._button_pins)):
            raise ApplicationError(u"com.example.invalid_argument", "No Button with ID {}".format(button))

    def get_button(self, button = None):
        """
        Get a Button status.
        """
        if button is not None:
            self._check_button_arg(button)
            return self._btn_status[button]
        else:
            return self._btn_status

    def _scan_buttons(self):
        for btn in range(0, len(self._button_pins)):
            pressed = GPIO.input(self._button_pins[btn]) == 1
            if self._btn_status[btn] != pressed:
                self._btn_status[btn] = pressed
                self.publish(u"com.example.device.{}.gpio.on_button".format(self._id), button=btn, pressed=pressed)
                if pressed:
                    log.msg("Button {} pressed".format(btn))
                else:
                    log.msg("Button {} released".format(btn))


def get_serial():
    """
    Get the Pi's serial number.
    """
    try:
        with open('/proc/cpuinfo') as f:
            for line in f.read().splitlines():
               if line.startswith('Serial'):
                   return line.split(':')[1].strip()[8:]
    except:
        pass
    return "00000000"


if __name__ == '__main__':

    # parse command line arguments
    #
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--debug", action="store_true",
                        help="Enable debug output.")

    parser.add_argument("--router", type=unicode, required=True,
                        help='URL of WAMP router to connect to.')

    parser.add_argument("--realm", type=unicode, default=u"realm1",
                        help='The WAMP realm to join on the router.')

    parser.add_argument("--id", type=unicode, default=None,
                        help='The Device ID to use. Default is to use the RaspberryPi Serial Number')

    args = parser.parse_args()

    log.startLogging(sys.stdout)

    if args.id is None:
        args.id = get_serial()

    log.msg("GpioBackend starting with ID {} ...".format(args.id))

    # install the "best" available Twisted reactor
    #
    reactor = install_reactor()
    log.msg("Running on reactor {}".format(reactor))

    extra = {
        'id': args.id,
 
         # these Pins are wired to LEDs
         "led_pins": [21, 22],

         # these Pins are wired to Buttons
         "button_pins": [17],

         # we will scan the GPIOs at this rate (Hz)
         "scan_rate": 50
    }

    runner = ApplicationRunner(url=args.router, realm=args.realm, extra=extra, debug=args.debug)
    runner.run(GpioBackend)
