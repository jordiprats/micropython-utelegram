#!/bin/bash

pkill screen

for file in main.py config.py utelegram.py;
do
    echo "refreshing $file"
    if [ -z "$1" ];
    then
        ampy --port /dev/ttyUSB0 rm $file
    fi
    ampy --port /dev/ttyUSB0 put $file
done