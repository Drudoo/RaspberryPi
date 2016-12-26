#!/bin/sh
echo -n "Configuring pin 17 as OUTPUT"
gpio -g mode 17 out
sleep 1
echo -n "."
sleep 1
echo -n "."
gpio export 17 out
echo "Done!"
echo "Starting HomeBridge"
homebridge