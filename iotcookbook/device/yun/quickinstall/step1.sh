#!/bin/sh

# upgrade the Yun's base image

opkg update
opkg install unzip
cd /tmp
wget http://downloads.arduino.cc/openwrtyun/1/YunSysupgradeImage_v1.5.3.zip
unzip YunSysupgradeImage_v1.5.3.zip
sysupgrade -v -n openwrt-ar71xx-generic-yun-16M-squashfs-sysupgrade.bin

# the Yun will automatically reboot here ..
