# Connecting the Pi's GPIOs to Crossbar.io

## Description

The Pi has a number of [GPIOs ](https://www.raspberrypi.org/documentation/usage/gpio/) which allow you to hook up actuators and sensors.

The example shows how to expose two LEDs and a button wired to the Pi's GPIOs via WAMP so you can turn on/off the LEDs and sense the button from **any other** WAMP component.

The code for the example consists of a backend written in Python and AutobahnPython using Twisted. The backend runs on the Pi and connects to Crossbar.io running on a network accessible from the Pi.

The backend exposes these procedures

* `com.example.device.<DEVICE ID>.gpio.set_led`
* `com.example.device.<DEVICE ID>.gpio.get_led`
* `com.example.device.<DEVICE ID>.gpio.toggle_led`
* `com.example.device.<DEVICE ID>.gpio.get_button`

and publishes event on these topics

* `com.example.device.<DEVICE ID>.gpio.on_led_set`
* `com.example.device.<DEVICE ID>.gpio.on_button`

Included with a frontend running in browsers. The frontend is written in JavaScript using AutobahnJS and connects to the same Crossbar.io router instance as the backend connects to. Consequently, the frontend is able to invoke the procedures exposed on the Pi and subscribe to events generated from there.


## How to run

If you don't have aleady, login to your Pi and install Autobahn:

```console
sudo pip install autobahn
```

> If you run a recent Raspbian, you are all set. If not, you might need to install [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) `sudo apt-get install python-dev python-rpi.gpio`


Copy the backend component from your computer to the Pi:

```console
scp gpio_backend.py pi@<IP of your Pi>:~/
```

and login to start the component

```
sudo python gpio_backend.py --router <WebSocket URL of your Crossbar.io Router>
```

> The backend has to run as root because it needs to access the GPIOs, which is a restricted operation. 


## Pointers

* http://pi.gadgetoid.com/pinout
* http://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/
* https://learn.adafruit.com/playing-sounds-and-using-buttons-with-raspberry-pi/install-python-module-rpi-dot-gpio




