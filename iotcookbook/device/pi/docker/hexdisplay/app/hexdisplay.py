# -*- coding: UTF-8 -*-

import six

from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

from Adafruit_LED_Backpack.HT16K33 import HT16K33


# Digit value to bitmask map.
#
REPLACEMENT = 0x00

DIGIT_VALUES = {
    u' ': 0x00,
    u'!': 0x82,
    u'"': 0x21,
    u'\'': 0x02,
    u'{': 0x39,
    u'}': 0x0f,
    u'-': 0x40,
    u'.': 0x80,
    u'0': 0x3f,
    u'1': 0x06,
    u'2': 0x5b,
    u'3': 0x4f,
    u'4': 0x66,
    u'5': 0x6d,
    u'6': 0x7d,
    u'7': 0x07,
    u'8': 0x7f,
    u'9': 0x6f,
    u'=': 0x48,
    u'?': 0x53,
    u'A': 0x77,
    u'B': 0x7c,
    u'C': 0x39,
    u'D': 0x5e,
    u'E': 0x79,
    u'F': 0x71,
    u'G': 0x6f,
    u'H': 0x76,
    u'I': 0x06,
    u'J': 0x1e,
    u'K': 0x76, # REPLACEMENT,
    u'L': 0x38,
    u'M': 0x54, # REPLACEMENT,
    u'N': 0x54,
    u'O': 0x3f,
    u'P': 0x73,
    u'Q': 0x67,
    u'R': 0x50,
    u'S': 0x6d,
    u'T': 0x78,
    u'U': 0x1c,
    u'V': 0x3e, # REPLACEMENT,
    u'W': 0x3e, # REPLACEMENT,
    u'X': 0x76, # REPLACEMENT,
    u'Y': 0x6e,
    u'Z': 0x5b, # REPLACEMENT,
    u'[': 0x39,
    u']': 0x0f,
    u'°': 0x63,
}


class HexDisplay(HT16K33):
    """
    Driver for 6-digit 7-segment display on the Crossbar.io IoT Starterkit.
    """

    TOTAL_DIGITS = 6
    """
    Total number of digits (1-8).
    """

    def set_clear(self):
        """
        Clear and refresh the display.
        """
        self.clear()
        self.write_display()

    def set_raw_digit(self, pos, value):
        """
        Set a digit to a raw value.
        """
        assert(pos in range(self.TOTAL_DIGITS))
        assert(type(value) in six.integer_types)

        self.buffer[pos * 2] = value & 0xFF

    def set_digit(self, pos, char, decimal=False):
        """
        Set a digit to a character. Note that this does not refresh the display.

        :param pos: The digit position (0-TOTAL_DIGITS-1).
        :type pos: int

        :param char: The digit char, a string of length 1, one of DIGIT_VALUES.
        :type char: str
        """
        assert(pos in range(self.TOTAL_DIGITS))
        assert(type(char) == six.text_type)

        char = char.strip().upper()
        bitmask = DIGIT_VALUES.get(char, 0x00)
        self.buffer[pos * 2] = bitmask & 0xFF
        if decimal:
            self.set_decimal(pos, True)

    def set_decimal(self, pos, enable):
        """
        Set decimal point on digit. Note that this does not refresh the display.

        :param pos: The digit position (0-TOTAL_DIGITS-1).
        :type pos: int

        :param enable: Flag to enable/disable decimal point.
        :type enable: bool
        """
        assert(pos in range(self.TOTAL_DIGITS))
        assert(type(enable) == bool)

        if enable:
            self.buffer[pos * 2] |= (1 << 7)
        else:
            self.buffer[pos * 2] &= ~(1 << 7)

    def set_message(self, message):
        """
        Set a message text on the display and refresh the display.
        """
        assert(type(message) == six.text_type)
        i = 0
        for c in message[:self.TOTAL_DIGITS]:
            self.set_digit(i, c)
            i += 1
        self.write_display()

    @inlineCallbacks
    def scroll_message(self, message, delay=150):
        assert(type(message) == six.text_type)
        _message = message + u' ' * self.TOTAL_DIGITS
        for i in range(len(message) + 1):
            self.set_message(_message[i:])
            yield sleep(delay / 1000.)


if __name__ == '__main__':

    # Test the display.

    from time import sleep

    display = HexDisplay(address=0x77)
    display.begin()
    display.clear()

    for i in range(256):
        for pos in range(6):
            display.buffer[pos * 2] = i & 0xFF
        display.write_display()
        print(u'0x{:x}'.format(i))
        sleep(2)

    for msg in [u'012345', u'6789AB', u'CDEF-_']:
        display.set_message(msg)
        sleep(1)

    for k in range(5):
        for i in range(6):
            display.clear()
            display.set_digit(i, u'{}'.format(i))
            display.write_display()
            sleep(.1)

    for k in range(5):
        for i in range(6):
            display.clear()
            display.set_decimal(i, True)
            display.write_display()
            sleep(.1)

    display.clear()
    display.write_display()
