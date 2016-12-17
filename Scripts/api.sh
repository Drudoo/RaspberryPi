#!/bin/bash


if [ "$(uname)" == "Darwin" ]; then
    realpath() {
    	[[ $1 = /* ]] && echo "$1" || echo "$PWD/"
	}
    MYDIR=$(realpath "$0")
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    MYDIR="$(dirname "$(realpath "$0")")"
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    MYDIR="$(dirname "$(realpath "$0")")"
fi

touch $MYDIR/api.log


currDate=$(date +"%m-%d-%y")
DNSfileName="DNS - "$currDate".txt"
ADSfileName="ADS - "$currDate".txt"

TIMEfileName="TIME - "$currDate".txt"

HOURLYfileName="HOURLY - "$currDate".txt"

echo $MYDIR
echo $DNSfileName

if [[ ! -f "$MYDIR/$DNSfileName" ]]; then
	touch "$MYDIR/$DNSfileName"
fi

if [[ ! -f "$MYDIR/$HOURLYfileName" ]]; then
	touch "$MYDIR/$HOURLYfileName"
fi

if [[ ! -f "$MYDIR/$ADSfileName" ]]; then
	touch "$MYDIR/$ADSfileName"
fi

if [[ ! -f "$MYDIR/$TIMEfileName" ]]; then
	touch "$MYDIR/$TIMEfileName"
fi

date +"%H%M" >> "$MYDIR/$TIMEfileName"

date +"%T - [Ads] - Getting API data from server"
date +"%T - [Ads] - Getting API data from server" >> $MYDIR/api.log
url=http://192.168.0.25/admin/api.php
value=$(curl -s "$url")
echo $value
date +"%T - [Ads] - Printing data to file" >> $MYDIR/api.log
echo $value | jq -r '.domains_being_blocked' > $MYDIR/api.txt
echo $value | jq -r '.dns_queries_today' >> $MYDIR/api.txt
echo $value | jq -r '.dns_queries_today' >> "$MYDIR/$DNSfileName"
echo $value | jq -r '.ads_blocked_today' >> $MYDIR/api.txt
echo $value | jq -r '.ads_blocked_today' >> "$MYDIR/$ADSfileName"
echo $value | jq -r '.ads_percentage_today' >> $MYDIR/api.txt


DNS=$(echo $value | jq -r '.dns_queries_today')
ADS=$(echo $value | jq -r '.ads_blocked_today')

DNS=$(echo $DNS | sed 's/\,/./')
ADS=$(echo $ADS | sed 's/\,/./')

echo $DNS","$ADS >> "$MYDIR/$HOURLYfileName"

date +"%T - [Ads] - Done..." >> $MYDIR/api.log

