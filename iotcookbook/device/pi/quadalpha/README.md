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

## Wifi Setup

In general, Wifi setup from the CLI isn't hard these days anymore .. see [here](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md) and [here](http://raspberrypi.stackexchange.com/questions/11631/how-to-setup-multiple-wifi-networks).

To configure your Wifi network, SSH into the Pi and edit the following file:

```console
sudo vi /etc/wpa_supplicant/wpa_supplicant.conf
```

For example, here is mine (passwords stripped):

```console
pi@raspberrypi:~ $ sudo cat /etc/wpa_supplicant/wpa_supplicant.conf
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    id_str="office"
    ssid="ap-office"
    psk="********"
    priority=5
}

network={
    id_str="home"
    ssid="ap-home"
    psk="********"
    priority=3
}

network={
    id_str="mobile"
    ssid="ap-mobile"
    psk="********"
    priority=1
}
```

> You can have multiple networks defined, and have priorities on networks as well (when multiple configured networks are in reach). Switching between networks only works for me when rebooting! There are also recipes for making that automatic using some scripts, eg [here](http://raspberrypi.stackexchange.com/questions/11631/how-to-setup-multiple-wifi-networks) - I haven't explored that path yet.

To scan for Wifi networks in reach:

```console
sudo iwlist wlan0 scan
```

To restart Wifi (without reboot):

```console
sudo ifdown wlan0
sudo ifup wlan0
```

To get the current Wifi configuration of the Wifi interface:

```console
ifconfig wlan0
```

To find a Pi on some network:

```console
nmap 192.168.43.*
```

Eg given above, this Pi (MAC `F4:F2:6D:14:1B:56`) will join one of the Wifi network (depending on which one is in reach):

* office: 192.168.1.142
* mobile: 192.168.43.105
* home: 192.168.55.104

### wicd

There is a curses based Wifi config app too:

```
sudo apt-get install wicd-curses
sudo wicd-curses
```

