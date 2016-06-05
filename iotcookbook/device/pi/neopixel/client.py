import time
import random
import Adafruit_ADS1x15
from neopixel import *

LED_COUNT      = 8       # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)


def show_level(strip, value):
	i = int(round(float(strip.numPixels()) * value))
	for k in range(strip.numPixels()):
		if k < i:
			strip.setPixelColor(k, Color(255, 222, 0))
		else:
			strip.setPixelColor(k, Color(0, 0, 0))
	strip.show()

if __name__ == '__main__':
	adc = Adafruit_ADS1x15.ADS1015()
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	strip.begin()

	while True:
		value = adc.read_adc(0, gain=4)
		print(value)
		show_level(strip, .5)
		time.sleep(.2)
