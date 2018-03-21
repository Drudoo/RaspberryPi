#!/bin/bash

function show_time () {
    num=$1
    min=0
    hour=0
    day=0
    if((num>59));then
        ((sec=num%60))
        ((num=num/60))
        if((num>59));then
            ((min=num%60))
            ((num=num/60))
            if((num>23));then
                ((hour=num%24))
                ((day=num/24))
            else
                ((hour=num))
            fi
        else
            ((min=num))
        fi
    else
        ((sec=num))
    fi
    echo "$hour:""$min:""$sec"
}

while true; do
	weather=$(curl -sS http://api.openweathermap.org/data/2.5/weather\?id\=2618425\&APPID\=<APIKEY>\&units\=metric)

	sunrise=$(echo $weather | jq -r '.sys .sunrise')
	sunset=$(echo $weather | jq -r '.sys .sunset')

	temp=$(echo $weather | jq -r '.main .temp')
	humidity=$(echo $weather | jq -r '.main .humidity')
	description=$(echo $weather | jq -r '.weather' | jq -r '.[] .description')
	icon=$(echo $weather | jq -r '.weather' | jq -r '.[] .icon')

	let srise="$sunrise+60*60*2"
	let sset="$sunset+60*60*2"

	echo $(date +%H:%M:%S) 'Sunrise:' $(show_time $srise) 'and Sunset:' $(show_time $sset)

	echo $sunrise > current.txt
	echo $sunset >> current.txt
	echo $temp > weather.txt
	echo $humidity >> weather.txt
	echo $description >> weather.txt
	echo $icon >> weather.txt

	sleep $[60 * 60]
done

