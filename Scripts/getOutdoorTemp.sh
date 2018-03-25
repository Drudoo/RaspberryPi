#!/bin/bash
ctemp=$'\xC2\xB0'
temp=$(curl -s '192.168.0.10' | jq -r .Temperature.Celsius | sed 's/\\[tn]//g')
/home/pi/pushover.sh -t "Outdoor temperature" "Today it's${temp}${ctemp}C outside" | xargs
