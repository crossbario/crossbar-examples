# Crossbar.io IoT Starterkit: Dispenser Demo

The frontend for this demo is hosted [here](https://cbdemo-eu-central-1.crossbar.io/dispenser/).


## Hardware Setup

The dispenser hardware consists of:

* 2 x mechanical actuator (Pi/BCM pins 13 and 19)
* 2 x LED (Pi/BCM pins 5 and 6)
* 2 x Button (Pi/BCM pins 20 and 21)

See here:

![](RP2_Pinout.png "RaspberryPi Pinout")


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
    ssid="SWEC16"
    key_mgmt=NONE
    priority=6
}

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

