###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Tavendo GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

import re
import sys
import argparse

from twisted.python import log
from twisted.internet import stdio
from twisted.internet.protocol import Protocol
from twisted.protocols.basic import LineReceiver

from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner


class XboxdrvProtocol(LineReceiver):

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


class XboxBridge(ApplicationSession):

    def onJoin(self, details):
        log.msg("Session ready: {}".format(details))
        self._xbox = self.config.extra
        self._xbox._session = self


def get_serial():
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

    xbox = XboxdrvProtocol(topic=u"io.crossbar.xbox.{}.ondata".format(args.id), debug=args.debug)
    stdio.StandardIO(xbox)

    runner = ApplicationRunner(url=args.router, realm=args.realm, extra=xbox, debug=args.debug)
    runner.run(XboxBridge)
