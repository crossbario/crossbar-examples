# Crossbar.io Votes Demo

This demo connects a Pi with a quad LED display and a button to our live voting demo.

## Hardware setup

> Pi expansion header pinouts can be found [here](https://pinout.xyz/)

The builtin display is wired like this:

* BCM 2, pin 3 => SDA
* BCM 3, pin 5 => SCL
* 5V, pin 4 => 5V
* GND, pin 6 => GND

To wire up the voting button should be wired like this:

* BCM 26, ping 37 => OUT
* 5V, pin 4 => 5V
* GND, pin 6 => GND

## Install as service

The example contains a systemd service unit which when installed can make the demo start automatically at system boot.

To install the service:

```console
make install
```

To `start`, `stop`, `restart` the service, get service `status` and `log`:

```console
make <COMMAND>
```
## Adafruit Library Code

This example contains code copied from:

* https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code
* https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/pull/94
* https://github.com/fschioler/Adafruit-Raspberry-Pi-Python-Code

All above code is licensed under a MIT like license. See [here](https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/blob/master/README.md).

The code might have been slightly modified and extended after we have copied it here.
