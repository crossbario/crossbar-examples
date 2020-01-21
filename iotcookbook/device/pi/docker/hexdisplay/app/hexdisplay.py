# -*- coding: UTF-8 -*-

import six

from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

from Adafruit_LED_Backpack.HT16K33 import HT16K33


# Digit value to bitmask map.
#
REPLACEMENT = 0x00

DIGIT_VALUES = {
    ' ': 0x00,
    '!': 0x82,
    '"': 0x21,
    '\'': 0x02,
    '{': 0x39,
    '}': 0x0f,
    '-': 0x40,
    '.': 0x80,
    '0': 0x3f,
    '1': 0x06,
    '2': 0x5b,
    '3': 0x4f,
    '4': 0x66,
    '5': 0x6d,
    '6': 0x7d,
    '7': 0x07,
    '8': 0x7f,
    '9': 0x6f,
    '=': 0x48,
    '?': 0x53,
    'A': 0x77,
    'B': 0x7c,
    'C': 0x39,
    'D': 0x5e,
    'E': 0x79,
    'F': 0x71,
    'G': 0x6f,
    'H': 0x76,
    'I': 0x06,
    'J': 0x1e,
    'K': 0x76, # REPLACEMENT,
    'L': 0x38,
    'M': 0x54, # REPLACEMENT,
    'N': 0x54,
    'O': 0x3f,
    'P': 0x73,
    'Q': 0x67,
    'R': 0x50,
    'S': 0x6d,
    'T': 0x78,
    'U': 0x1c,
    'V': 0x3e, # REPLACEMENT,
    'W': 0x3e, # REPLACEMENT,
    'X': 0x76, # REPLACEMENT,
    'Y': 0x6e,
    'Z': 0x5b, # REPLACEMENT,
    '[': 0x39,
    ']': 0x0f,
    '°': 0x63,
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
        _message = message + ' ' * self.TOTAL_DIGITS
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
        print('0x{:x}'.format(i))
        sleep(2)

    for msg in ['012345', '6789AB', 'CDEF-_']:
        display.set_message(msg)
        sleep(1)

    for k in range(5):
        for i in range(6):
            display.clear()
            display.set_digit(i, '{}'.format(i))
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
