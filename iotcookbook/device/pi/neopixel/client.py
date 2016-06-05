import time
import random
from neopixel import *

LED_COUNT      = 8       # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbowCycle(strip, wait_ms=5, iterations=5):
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel(((i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def randomCycle(strip):
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
	strip.show()
	time.sleep(50./1000.)

def levelMeter(strip, value):
	i = int(round(float(strip.numPixels()) * value))
	for k in range(strip.numPixels()):
		if k < i:
			strip.setPixelColor(k, Color(255, 222, 0))
		else:
			strip.setPixelColor(k, Color(0, 0, 0))
	strip.show()
	time.sleep(50./1000.)

if __name__ == '__main__':
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	strip.begin()

	while True:
		#rainbowCycle(strip)
		#randomCycle(strip)
		levelMeter(strip, .5)

