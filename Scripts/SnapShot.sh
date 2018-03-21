#!/bin/bash

IN_LOCAL=snapImg.jpg
OUT_REMOTE=snapImg.jpg

USER=<ftp username>
PASSWD=<ftp password>
SERVERIP=<ftp url>

DATE=`date +%Y-%m-%d_%H-%M-%S`

TIME=$(date +"%d/%m/%Y")
HOUR=$(date +"%R")

# IFS=$'\n' read -d '' -r -a lines < weather.txt

mapfile -t lines < weather.txt

raspistill -o snapImg.jpg -w 1000 -h 1000 -rot 90 -hf -vf & ./disablecameraled.py

sleep 10

C=${lines[0]}
F=$(echo "$C*1.8+32" | bc)
humidity=${lines[1]}
description=${lines[2]}
icon=Icons/${lines[3]}.png
description=$(echo -e $description | sed -r 's/\<./\U&/g')
imgText="$description ${C}°C - ${F}°F - Humidity: ${humidity}%"

# convert snapImg.jpg -font Helvetica \
#	-draw "rectangle 0 950 1000 1000" -fill black \
#	-pointsize 20 -fill white -annotate +800+980 \
#	$TIME \
#	-pointsize 20 -fill white -annotate +930+980 \
#	$HOUR \
#	-pointsize 20 -fill white -annotate +20+980 \
#	'Raspberry Pi Camera (W:1000px, H:1000px)' \
# snapImg.jpg

convert snapImg.jpg -font Helvetica -draw "rectangle 0 950 1000 1000" -fill black -pointsize 20 -fill white -annotate +800+980 $TIME -pointsize 20 -fill white -annotate +930+980 $HOUR -pointsize 20 -fill white -annotate +50+980 "$imgText" snapImgWithText.jpg
convert snapImgWithText.jpg $icon -geometry +0+950 -composite snapImg.jpg

scp snapImg.jpg <ssh upload location eg. UserName.com@ssh.UserName.com:/www/image/snapImg.jpg>
scp snapImg.jpg <ssh upload location eg. UserName.com@ssh.UserName.com:/www/image/$DATE.jpg>
