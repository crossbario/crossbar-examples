https://github.com/adafruit/Adafruit_NeoPixel
https://learn.adafruit.com/adafruit-neopixel-uberguide/arduino-library

+LED_COUNT      = 8       # Number of LED pixels.
+LED_PIN        = 12      # GPIO pin connected to the pixels (must support PWM!).

    sudo apt-get update
    sudo apt-get install build-essential python-dev git scons swig

    git clone https://github.com/jgarff/rpi_ws281x.git
    cd rpi_ws281x
    scons

    cd python
    sudo python setup.py install

