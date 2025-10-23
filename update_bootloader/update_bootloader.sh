#!/bin/bash

adafruit-nrfutil --verbose dfu serial --package nice_nano_bootloader-0.9.2_s140_6.1.1.zip -p /dev/ttyACM0 -b 115200 --singlebank --touch 1200
