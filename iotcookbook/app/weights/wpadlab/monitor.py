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

from twisted.internet.defer import inlineCallbacks
from twisted.internet.serialport import SerialPort
from twisted.protocols.basic import LineReceiver

from autobahn.util import utcnow
from autobahn.twisted.wamp import ApplicationSession


class WpadSerial(LineReceiver):

    """
    MCU serial communication protocol.
    """

    # need a reference to our WS-MCU gateway factory to dispatch PubSub events
    #
    def __init__(self, session, debug=False):
        self._debug = debug
        self._session = session
        self._last = None
        self._last_event = None
        self._id = 1
        self._wpad_id = session.config.extra['wpad_id']

    def get_last(self):
        return self._last_event

    @inlineCallbacks
    def connectionMade(self):
        print('Serial port connected.')
        yield self._session.register(self.get_last, u"io.crossbar.demo.wpad.{}.get_last".format(self._wpad_id))

    def lineReceived(self, line):
        if self._debug:
            print("Serial RX: {0}".format(line))

        pins = range(8)

        try:
            # parse data received from MCU
            ##
            data = [int(x) for x in line.split(',')]
        except ValueError:
            print('Unable to parse value {0}'.format(line))
        else:
            if not self._last:
                self._last = data
            else:
                changed = False
                for i in range(len(data)):
                    #print i
                    if i in pins:
                        if abs(data[i] - self._last[i]) > 3:
                            changed = True
                            break

                if changed:
                    payload = {
                        u'id': self._id,
                        u'timestamp': utcnow(),
                        u'values': [1023 - data[p] for p in pins]
                    }

                    self._session.publish(u"io.crossbar.demo.wpad.{}.on_change".format(self._wpad_id), payload)
                    self._last_event = payload
                    self._last = data
                    self._id += 1


class WpadMonitor(ApplicationSession):

    """
    MCU WAMP application component.
    """

    def onJoin(self, details):

        port = self.config.extra['port']
        baudrate = self.config.extra['baudrate']
        debug = self.config.extra['debug']

        self._serial_proto = WpadSerial(self, debug)

        try:
            self._serial_port = SerialPort(self._serial_proto, port, reactor, baudrate=baudrate)
        except Exception as e:
            print('Could not open serial port: {0}'.format(e))
            self.leave()

        print("Wpad ready! Configuration: {}".format(self.config.extra))


if __name__ == '__main__':

    import sys
    import argparse

    # parse command line arguments
    ##
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--debug", action="store_true",
                        help="Enable debug output.")

    parser.add_argument("--baudrate", type=int, default=115200, choices=[300, 1200, 2400, 4800, 9600, 19200, 57600, 115200],
                        help='Serial port baudrate.')

    parser.add_argument("--port", type=str, default='/dev/ttyACM0',
                        help='Serial port to use (e.g. 3 for a COM port on Windows, /dev/ttyATH0 for Arduino Yun, /dev/ttyACM0 for Serial-over-USB on RaspberryPi.')

    parser.add_argument("--router", type=str, default='ws://localhost:8080/ws',
                        help='Connect to this WAMP router.')

    parser.add_argument("--realm", type=str, default='realm1',
                        help='Realm to attach to.')

    parser.add_argument("--wpad_id", type=str, default='1',
                        help='Weighing pad ID.')

    args = parser.parse_args()

    try:
        # on Windows, we need port to be an integer
        args.port = int(args.port)
    except ValueError:
        pass

    from twisted.python import log
    log.startLogging(sys.stdout)

    # import Twisted reactor
    #
    if sys.platform == 'win32':
        # on windows, we need to use the following reactor for serial support
        # http://twistedmatrix.com/trac/ticket/3802
        ##
        from twisted.internet import win32eventreactor
        win32eventreactor.install()

    from twisted.internet import reactor
    print("Using Twisted reactor {0}".format(reactor.__class__))

    # run WAMP application component
    #
    from autobahn.twisted.wamp import ApplicationRunner

    extra = {
        'wpad_id': args.wpad_id,
        'port': args.port,
        'baudrate': args.baudrate,
        'debug': args.debug
    }
    runner = ApplicationRunner(args.router, args.realm, extra=extra)

    # start the component and the Twisted reactor ..
    #
    runner.run(WpadMonitor)
