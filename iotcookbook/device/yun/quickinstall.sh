#!/bin/sh

uci add fstab mount
uci set fstab.@mount[0].target=/overlay
uci set fstab.@mount[0].device=/dev/sda2
uci set fstab.@mount[0].fstype=ext4
uci set fstab.@mount[0].enabled=1
uci set fstab.@mount[0].enabled_fsck=0
uci set fstab.@mount[0].options=rw,sync,noatime,nodiratime
uci commit

opkg update
opkg install unzip
cd /tmp
wget http://downloads.arduino.cc/openwrtyun/1/YunSysupgradeImage_v1.5.3.zip
unzip YunSysupgradeImage_v1.5.3.zip
sysupgrade -v -n openwrt-ar71xx-generic-yun-16M-squashfs-sysupgrade.bin
