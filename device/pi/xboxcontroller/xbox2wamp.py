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


class XboxdrvProtocol(LineReceiver):
    """
    Protocol for parsing output from Xboxdrv.
    """

    delimiter = '\n'

    def __init__(self, topic, debug=False):
        self._debug = debug
        self._session = None
        self._last = None
        self._topic = topic

    def connectionMade(self):
        log.msg('Xboxdrv connected')

    def lineReceived(self, line):
        if self._debug:
            log.msg("XboxdrvProtocol line received: {}".format(line))

        # Parse lines received from Xboxdrv. Lines look like:
        #
        # X1:  -764 Y1:  4198  X2:   385 Y2:  3898  du:0 dd:0 dl:0 dr:0  back:0 guide:0 start:0  TL:0 TR:0  A:0 B:0 X:0 Y:0  LB:0 RB:0  LT:  0 RT:  0
        #
        try:
            parts = re.split(r"[:\s]+", line)

            data = {}
            for i in range(0, len(parts) - 2, 2):

                attr = parts[i]
                val = parts[i + 1]

                data[attr] = int(val)

        except Exception as e:
            if self._debug:
                log.msg("Could not parse line: {}".format(e))
        else:
            changed = {}
            if self._last:
                for k in data:
                    if data[k] != self._last[k]:
                        changed[k] = data[k]
            else:
                changed = data

            if self._session and len(changed):
                self._session.publish(self._topic, data)
                if True or self._debug:
                    log.msg("XboxdrvProtocol event published to {}: {}".format(self._topic, changed))

            self._last = data


class Xbox2Wamp(ApplicationSession):
    """
    Connects Xbox gamepad controller to WAMP.
    """

    @inlineCallbacks
    def onJoin(self, details):
        log.msg("Xbox2Wamp connected.")

        extra = self.config.extra

        self._id = extra['id']
        self._xbox = extra['xbox']
        self._xbox._session = self

        for proc in [self.get_data]:
            uri = u'com.example.device.{}.gamepad.{}'.format(self._id, proc.__name__)
            yield self.register(proc, uri)
            log.msg("Registered {}".format(uri))

        log.msg("Xbox2Wamp ready.")

    def get_data(self):
        return self._xbox._last 


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
                        help='Client ID.')

    args = parser.parse_args()

    log.startLogging(sys.stdout)

    if args.id is None:
        args.id = get_serial()

    log.msg("Xbox2Wamp bridge starting with ID {} ...".format(args.id))

    # install the "best" available Twisted reactor
    #
    from autobahn.twisted.choosereactor import install_reactor
    reactor = install_reactor()
    log.msg("Running on reactor {}".format(reactor))

    xbox = XboxdrvProtocol(topic=u"com.example.device.{}.gamepad.on_data".format(args.id), debug=args.debug)
    stdio.StandardIO(xbox)

    extra = {
        'id': args.id,
        'xbox': xbox
    }

    runner = ApplicationRunner(url=args.router, realm=args.realm, extra=extra, debug=args.debug)
    runner.run(Xbox2Wamp)
