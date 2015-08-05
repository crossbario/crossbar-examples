#!/bin/sh

#cp /.extroot.md5sum /mnt/sda2/etc/extroot.md5sum
rm -f /mnt/sda2/etc/extroot.md5sum

# activate extroot from SD card

uci add fstab mount
uci set fstab.@mount[0].target=/overlay
uci set fstab.@mount[0].device=/dev/sda2
uci set fstab.@mount[0].fstype=ext4
uci set fstab.@mount[0].enabled=1
uci set fstab.@mount[0].enabled_fsck=0
uci set fstab.@mount[0].options=rw,sync,noatime,nodiratime
uci commit

reboot
