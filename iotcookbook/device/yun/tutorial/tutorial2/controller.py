import sys
from twisted.protocols.basic import LineReceiver
from twisted.internet.serialport import SerialPort
from twisted.internet.task import LoopingCall

# adjust this for your setup:

# Serial port to use (e.g. 2 (the integer) for a COM port ('COM3' here) on Windows,
# /dev/ttyATH0 for Arduino Yun or /dev/ttyACM0 for Serial-over-USB from Linux

SERIAL_PORT = "/dev/ttyATH0"
# SERIAL_PORT = "/dev/ttyACM0"
# SERIAL_PORT = 2

SERIAL_BAUDRATE = 115200


class MySerialBridge(LineReceiver):

    def connectionMade(self):
        print('Serial port connected.')

    def lineReceived(self, line):
        try:
            data = [int(x) for x in line.split(',')]
        except ValueError:
            print('Unable to parse line: {0}'.format(line))
        else:
            btn1, pot1 = data[0:2]

            # if button pressed, or analog value > 400, turn on LED
            if btn1 or pot1 > 400:
                self.transport.write("1\n")
            else:
                self.transport.write("0\n")


if __name__ == '__main__':

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

    # create instance of out serial protocol
    serial_proto = MySerialBridge()

    # create serial port: adjust for serial device / baudrate
    serial_port = SerialPort(serial_proto, SERIAL_PORT, reactor, baudrate=SERIAL_BAUDRATE)

    reactor.run()
