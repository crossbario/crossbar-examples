#!/usr/bin/python

import time
from Adafruit_LEDBackpack import LEDBackpack

# ===========================================================================
# Quad Alphabumeric Display
# Handles a display consisting of one or more 4-digit segments.
#
# Products:
# http://www.adafruit.com/products/1911
# http://www.adafruit.com/products/1912
# ===========================================================================

class QuadAlphanum:
  disp = []
  maxDigit = 0
  debug = False

  # The pixel matrix has been copied from the Adafruit Arduino library.
  alphafonttable = [
	  0b0000000000000001,
	  0b0000000000000010,
	  0b0000000000000100,
	  0b0000000000001000,
	  0b0000000000010000,
	  0b0000000000100000,
	  0b0000000001000000,
	  0b0000000010000000,
	  0b0000000100000000,
	  0b0000001000000000,
	  0b0000010000000000,
	  0b0000100000000000,
	  0b0001000000000000,
	  0b0010000000000000,
	  0b0100000000000000,
	  0b1000000000000000,
	  0b0000000000000000,
	  0b0000000000000000,
	  0b0000000000000000,
	  0b0000000000000000,
	  0b0000000000000000,
	  0b0000000000000000,
	  0b0000000000000000,
	  0b0000000000000000,
	  0b0001001011001001,
	  0b0001010111000000,
	  0b0001001011111001,
	  0b0000000011100011,
	  0b0000010100110000,
	  0b0001001011001000,
	  0b0011101000000000,
	  0b0001011100000000,
	  0b0000000000000000, #  
	  0b0000000000000110, # !
	  0b0000001000100000, # "
	  0b0001001011001110, # #
	  0b0001001011101101, # $
	  0b0000110000100100, # %
	  0b0010001101011101, # &
	  0b0000010000000000, # '
	  0b0010010000000000, # (
	  0b0000100100000000, # )
	  0b0011111111000000, # *
	  0b0001001011000000, # +
	  0b0000100000000000, # ,
	  0b0000000011000000, # -
	  0b0100000000000000, # .
	  0b0000110000000000, # /
	  0b0000110000111111, # 0
	  0b0000000000000110, # 1
	  0b0000000011011011, # 2
	  0b0000000010001111, # 3
	  0b0000000011100110, # 4
	  0b0010000001101001, # 5
	  0b0000000011111101, # 6
	  0b0000000000000111, # 7
	  0b0000000011111111, # 8
	  0b0000000011101111, # 9
	  0b0001001000000000, # :
	  0b0000101000000000, # ;
	  0b0010010000000000, # <
	  0b0000000011001000, # =
	  0b0000100100000000, # >
	  0b0001000010000011, # ?
	  0b0000001010111011, # @
	  0b0000000011110111, # A
	  0b0001001010001111, # B
	  0b0000000000111001, # C
	  0b0001001000001111, # D
	  0b0000000011111001, # E
	  0b0000000001110001, # F
	  0b0000000010111101, # G
	  0b0000000011110110, # H
	  0b0001001000000000, # I
	  0b0000000000011110, # J
	  0b0010010001110000, # K
	  0b0000000000111000, # L
	  0b0000010100110110, # M
	  0b0010000100110110, # N
	  0b0000000000111111, # O
	  0b0000000011110011, # P
	  0b0010000000111111, # Q
	  0b0010000011110011, # R
	  0b0000000011101101, # S
	  0b0001001000000001, # T
	  0b0000000000111110, # U
	  0b0000110000110000, # V
	  0b0010100000110110, # W
	  0b0010110100000000, # X
	  0b0001010100000000, # Y
	  0b0000110000001001, # Z
	  0b0000000000111001, # [
	  0b0010000100000000, # 
	  0b0000000000001111, # ]
	  0b0000110000000011, # ^
	  0b0000000000001000, # _
	  0b0000000100000000, # `
	  0b0001000001011000, # a
	  0b0010000001111000, # b
	  0b0000000011011000, # c
	  0b0000100010001110, # d
	  0b0000100001011000, # e
	  0b0000000001110001, # f
	  0b0000010010001110, # g
	  0b0001000001110000, # h
	  0b0001000000000000, # i
	  0b0000000000001110, # j
	  0b0011011000000000, # k
	  0b0000000000110000, # l
	  0b0001000011010100, # m
	  0b0001000001010000, # n
	  0b0000000011011100, # o
	  0b0000000101110000, # p
	  0b0000010010000110, # q
	  0b0000000001010000, # r
	  0b0010000010001000, # s
	  0b0000000001111000, # t
	  0b0000000000011100, # u
	  0b0010000000000100, # v
	  0b0010100000010100, # w
	  0b0010100011000000, # x
	  0b0010000000001100, # y
	  0b0000100001001000, # z
	  0b0000100101001001, # {
	  0b0001001000000000, # |
	  0b0010010010001001, # }
	  0b0000010100100000, # ~
	  0b0011111111111111
  ]

  # Constructor
  def __init__(self, address=0x70, segments=1, debug=False):
    "Construct a display consisting of one or more 4-digit segments."
    # Save the upper limit for convenience
    self.maxDigit = 4 * segments
    self.debug = debug
    for segment in range(segments):
      addr = address + segment
      if (debug):
        print "Initializing a new instance of LEDBackpack at 0x%02X" % addr
      self.disp.append( LEDBackpack(address=addr, debug=debug) )

  def writeDigitRaw(self, value, pos, update=True):
    "Sets a digit using a raw 16-bit value"
    if (pos < 0 or pos >= self.maxDigit):
      # The position is out of range: To be expected by "setMessage()"
      return
    # Set the appropriate character
    self.disp[pos/4].setBufferRow(pos%4, value, update)

  def writeDigitAscii(self, char, pos, dot=False, update=True):
    "Lookup pixels from ascii table."
    if ord(char) < 0 or ord(char) > 127:
      if (self.debug):
        print "Invalid character: " + ord(char)
      return
    # Lookup and convert to font
    font = self.alphafonttable[ord(char)]
    if (dot):
      font |= (1<<14)
    self.writeDigitRaw(font, pos, update)

  def setMessage(self, text, pos=0):
    "Write a message on the display. No scroll. Return next free position."
    for char in text:
      if char == '.' and pos > 0 and pos <= self.maxDigit:
        # Dot: Update previous digit with a dot instead of writing a new letter.
        buffer = self.disp[(pos-1)/4].getBuffer()
        # Retrieved data has "font" format, not ASCII
        font = buffer[(pos-1)%4]
        # Set the dot
        font |= (1<<14)
        # Rewrite the last letter as a modified "font"
        self.writeDigitRaw(font, pos-1, False)
      else:
        # Normal case
        self.writeDigitAscii(char, pos, False, False)
        pos += 1
    self.writeDisplay()
    return pos

  def scrollMessage(self, text, scrollSpeed=0.3):
    "Scroll a message across the display."
    for char in text:
      if char == '.':
        # Dot: Update last digit with dot instead of writing new letter.
        buffer = self.disp[(self.maxDigit-1)/4].getBuffer()
        # Retrieved data has "font" format, not ASCII
        font = buffer[(self.maxDigit-1)%4]
        # Set the dot
        font |= (1<<14)
        # Rewrite the last letter as a modified "font"
        self.writeDigitRaw(font, self.maxDigit-1, True)
        # Do not sleep to ensure a semmingly fixed scroll speed
      else:
        # Normal case
        self.scrollLetter(char)
        time.sleep(scrollSpeed)

  def scrollLetter(self, char, dot=False):
    "Scroll the display and write the last letter"
    # Scroll all characters without updating the segments
    self.shiftLeft()
    # Write last character without updating the last segment
    self.writeDigitAscii(char, self.maxDigit-1, dot, update=False)
    # Update all segments
    self.writeDisplay()

  def shiftLeft(self):
    buffer = self.disp[0].getBuffer()
    for segment in range(0, len(self.disp)):
      for x in range (0, 3):
        # Shift 3 first columns of segment, no update during shift
        self.disp[segment].setBufferRow(x, buffer[x+1], False)
      if (segment + 1 < len(self.disp)):
        # Unless this is th last digit:
        # Transfer first column of next segment and update
        next_buffer = self.disp[segment+1].getBuffer()
        self.disp[segment].setBufferRow(3, next_buffer[0], False)
        buffer = next_buffer

  def writeDisplay(self):
    """Explicitely update the display.
    Used if you have written to the buffer with no update.
    """
    for segment in self.disp:
      segment.writeDisplay()

  def clear(self):
    "Clears the entire display"
    for segment in self.disp:
      segment.clear()

  def setBrightness(self, brightness):
    "Set brightness for all displays"
    for segment in self.disp:
      segment.setBrightness(brightness)

  # No use to handle multiple blinking segments:
  # They will never blink in sync anyway.

if __name__ == '__main__':
  "Self test / demo."
  screen = QuadAlphanum(0x77, 1, True)
  screen.setMessage("TEST.")
  time.sleep(2)
  screen.clear()
  screen.setMessage("fixed", 1)
  time.sleep(2)
  screen.scrollMessage(" and scrolling text.")
  for brightness in range (15, 0, -1):
    time.sleep(0.25)
    screen.setBrightness(brightness)
  screen.clear()
  screen.setMessage("Done.")
  screen.setBrightness(15)
