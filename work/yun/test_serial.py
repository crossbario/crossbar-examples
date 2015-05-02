import logging
from collections import deque
import serial

try:
    import asyncio
except ImportError:
    import trollius as asyncio


class SerialLineProtocol:
    """
    Hook up to serial ports. See: http://pythonhosted.org//pyserial/
    """

    def __init__(self, port='/dev/ttyATH0', baudrate=9600):
        self._port = port
        self._baudrate = baudrate
        self._fd = serial.Serial(port, baudrate, timeout=0, writeTimeout=0)
        self._receive_buffer = []

        self._transmit_buffer = deque()

        loop = asyncio.get_event_loop()

        # watch the serial port's FD under asyncio
        # https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.BaseEventLoop.add_reader
        loop.add_reader(self._fd, self._readable)

    def _readable(self):
        while self._fd.inWaiting():
            b = self._fd.read(1)
            if b == "\n":
                self.line_received(''.join(self._receive_buffer))
                self._receive_buffer = []
            else:
                self._receive_buffer.append(b)

    def line_received(self, line):
        logging.info("SerialLineProtocol.line_received: {}".format(line))

    def _writable(self):
        try:
            c = self._transmit_buffer.popleft()
            self._fd.write(c)
        except IndexError:
            loop.remove_writer(self._fd)

    def send_line(self, line):
        for c in line:
            self._transmit_buffer.append(c)
        self._transmit_buffer.append(b"\n")
        loop.add_writer(self._fd, self._writable)



class MySerialLineProtocol(SerialLineProtocol):

    def line_received(self, line):
        print("Received: {}".format(line))
        self.send_line("50")


logging.basicConfig(level=logging.DEBUG)

proto = MySerialLineProtocol(port='/dev/ttyATH0', baudrate=9600)

loop = asyncio.get_event_loop()
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.close()
