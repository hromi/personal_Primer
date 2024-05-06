#!/bin/bash
/sbin/dhclient usb0
/usr/bin/autossh -M 0 -N -R 2220:localhost:22 mame@mame.lesen.digital -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3"
