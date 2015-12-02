import sys
from twisted.internet.defer import inlineCallbacks
from twisted.protocols.basic import LineReceiver
from twisted.internet.serialport import SerialPort
from autobahn.twisted.wamp import ApplicationSession
from autobahn import wamp

# adjust this for your setup:


# Serial port to use (e.g. 2 (the integer) for a COM port ('COM3' here) on Windows,
# /dev/ttyATH0 for Arduino Yun or /dev/ttyACM0 for Serial-over-USB from Linux

SERIAL_PORT = "/dev/ttyATH0"
# SERIAL_PORT = "/dev/ttyACM0"
# SERIAL_PORT = 2

SERIAL_BAUDRATE = 115200

# connecting to Crossbar.io
ROUTER = "ws://192.168.1.130:8080/ws"
REALM = "realm1"


class MySerialBridge(LineReceiver):

    def __init__(self, session):
        self._session = session
        self._last = None
        self._led = False

    @inlineCallbacks
    def connectionMade(self):
        print("Serial port connected.")

        # turn off LED to start from a known state
        self.transport.write("0\n")

        yield self._session.register(self)
        print("Procedures registered.")

    def lineReceived(self, line):
        try:
            data = [int(x) for x in line.split(',')]
        except ValueError:
            print("Unable to parse line: {0}".format(line))
        else:
            print(data)
            self._last = data
            self._session.publish(u"io.crossbar.demo.yun.tutorial3.on_sensors", data)

    @wamp.register(u"io.crossbar.demo.yun.tutorial3.get_sensors")
    def get_sensor_vals(self):
        return self._last

    @wamp.register(u"io.crossbar.demo.yun.tutorial3.set_led")
    def set_led(self, value):
        if value:
            if not self._led:
                self.transport.write("1\n")
                self._led = True
                self._session.publish(u"io.crossbar.demo.yun.tutorial3.on_led", self._led)
                return True
            else:
                return False
        else:
            if self._led:
                self.transport.write("0\n")
                self._led = False
                self._session.publish(u"io.crossbar.demo.yun.tutorial3.on_led", self._led)
                return True
            else:
                return False

    @wamp.register(u"io.crossbar.demo.yun.tutorial3.get_led")
    def get_led(self):
        return self._led


class MySerialBridgeSession(ApplicationSession):

    def onJoin(self, details):
        print("Session connected")

        # create instance of out serial protocol
        serial_proto = MySerialBridge(self)

        # create serial port: adjust for serial device / baudrate
        try:
            from twisted.internet import reactor
            serial_port = SerialPort(serial_proto, SERIAL_PORT, reactor, baudrate=SERIAL_BAUDRATE)
        except Exception as e:
            print('Could not open serial port: {0}'.format(e))
            self.leave()

        print("Bridge ready!")


if __name__ == '__main__':

    import sys
    from twisted.python import log
    log.startLogging(sys.stdout)

    # import Twisted reactor
    #
    if sys.platform == 'win32':
        # on Windows, we need to use the following reactor for serial support
        # http://twistedmatrix.com/trac/ticket/3802
        #
        from twisted.internet import win32eventreactor
        win32eventreactor.install()

    from twisted.internet import reactor
    print("Using Twisted reactor {0}".format(reactor.__class__))

    from autobahn.twisted.wamp import ApplicationRunner

    runner = ApplicationRunner(ROUTER, REALM)
    runner.run(MySerialBridgeSession)
