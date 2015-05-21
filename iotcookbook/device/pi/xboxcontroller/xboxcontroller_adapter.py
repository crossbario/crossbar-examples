# Copyright (C) Tavendo GmbH. Open-source licensed under the
# MIT License (http://opensource.org/licenses/MIT)

import re
import sys
import argparse

from twisted.python import log
from twisted.internet import stdio
from twisted.internet.defer import inlineCallbacks
from twisted.internet.protocol import Protocol
from twisted.protocols.basic import LineReceiver

from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner


class XboxdrvReceiver(LineReceiver):
    """
    Protocol for parsing output from Xboxdrv.
    """

    delimiter = '\n'

    def __init__(self, debug=False):
        self._debug = debug
        self._session = None
        self._last = None

    def connectionMade(self):
        log.msg('XboxdrvReceiver connected')

    def lineReceived(self, line):
        if self._debug:
            log.msg("XboxdrvReceiver line received: {}".format(line))

        # Parse lines received from Xboxdrv. Lines look like:
        # X1:  -764 Y1:  4198  X2:   385 Y2:  3898  du:0 dd:0 dl:0 dr:0  back:0 guide:0 start:0  TL:0 TR:0  A:0 B:0 X:0 Y:0  LB:0 RB:0  LT:  0 RT:  0
        try:
            parts = re.split(r"[:\s]+", line)

            data = {}
            for i in range(0, len(parts) - 2, 2):

                attr = parts[i]
                val = parts[i + 1]

                data[attr] = int(val)

        except Exception as e:
            if self._debug:
                log.msg("XboxdrvReceiver: could not parse line '{}'".format(e))
        else:
            # determine change set
            changed = {}
            if self._last:
                for k in data:
                    if data[k] != self._last[k]:
                        changed[k] = data[k]
            else:
                changed = data

            # if WAMP session is active and change set is non-empty,
            # forward the controller data to the WAMP session
            if len(changed):
                if self._session:
                    self._session.on_data(data)
    
                if self._debug:
                    log.msg("XboxdrvReceiver event data: {}".format(changed))

                self._last = data


class XboxControllerAdapter(ApplicationSession):
    """
    Connects Xbox gamepad controller to WAMP.
    """

    @inlineCallbacks
    def onJoin(self, details):
        # the component has now joined the realm on the WAMP router
        log.msg("XboxControllerAdapter connected.")

        # get custom configuration
        extra = self.config.extra

        # Device ID and auxiliary info
        self._id = extra['id']
        self._xbox = extra['xbox']
        self._xbox._session = self

        # register methods on this object for remote calling via WAMP
        for proc in [self.get_data]:
            uri = u'io.crossbar.examples.iot.devices.pi.{}.xboxcontroller.{}'.format(self._id, proc.__name__)
            yield self.register(proc, uri)
            log.msg("XboxControllerAdapter registered procedure {}".format(uri))

        # signal we are done with initializing our component
        self.publish(u'io.crossbar.examples.iot.devices.pi.{}.xboxcontroller.on_ready'.format(self._id))
        log.msg("XboxControllerAdapter ready.")

    def get_data(self):
        """
        Get current controller state.
        """
        return self._xbox._last 

    def on_data(self, data):
        """
        Hook that fires when controller state has changed.
        """
        uri = u'io.crossbar.examples.iot.devices.pi.{}.xboxcontroller.on_data'.format(self._id)
        self.publish(uri, data)
        log.msg("XboxControllerAdapter event published to {}: {}".format(uri, data))


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

    parser.add_argument("--realm", type=unicode, default=u"iot_cookbook",
                        help='The WAMP realm to join on the router.')

    parser.add_argument("--id", type=unicode, default=None,
                        help='The Device ID to use. Default is to use the RaspberryPi Serial Number')

    args = parser.parse_args()

    # start logging to stdout
    #
    log.startLogging(sys.stdout)

    # get the Pi's serial number (allow override from command line)
    #
    if args.id is None:
        args.id = get_serial()

    log.msg("XboxControllerAdapter starting with ID {} ...".format(args.id))

    # install the "best" available Twisted reactor
    #
    from autobahn.twisted.choosereactor import install_reactor
    reactor = install_reactor()
    log.msg("Running on reactor {}".format(reactor))

    # used to receive and parse data from Xboxdrv
    #
    xbox = XboxdrvReceiver(debug=args.debug)
    stdio.StandardIO(xbox)

    # custom configuration data
    #
    extra = {
        # device ID
        'id': args.id,

        # our WAMP component needs access to the Xboxdrv receiver
        'xbox': xbox
    }

    # create and start app runner for our app component ..
    #
    runner = ApplicationRunner(url=args.router, realm=args.realm, extra=extra, debug=args.debug)
    runner.run(XboxControllerAdapter)
