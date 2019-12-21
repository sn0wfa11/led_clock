#!/bin/bash
/etc/init.d/led_clock stop
cd /root/git/led_clock
/usr/bin/git pull
/etc/init.d/led_clock start

