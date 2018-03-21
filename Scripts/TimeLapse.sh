#!/bin/bash

# nohup bash suncalc.sh & nohup bash SnapShot.sh &

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

while [[ true ]]; do
	# IFS=$'\n' read -d '' -r -a lines < current.txt

	mapfile -t lines < current.txt

	let sunrise="${lines[0]}+60*60*2"
	let sunset="${lines[1]}+60*60*2"

	# echo "Sunrise is at" $(show_time $sunrise) "and sunset is at" $(show_time $sunset)

	let currentTime="$(date +%s)+60*60*2"

	if [[ $currentTime -ge $sunrise ]]; then
		if [[ $currentTime -le $sunset ]]; then
			echo $(show_time $currentTime) "- Daytime"
			bash SnapShot.sh
			sleep 44
		fi
	fi

	if [[ $currentTime -lt $sunrise ]]; then
		echo $(show_time $currentTime) "- Nightime"
		bash SnapShot5.sh
		sleep 39
	fi

	if [[ $currentTime -gt $sunset ]]; then
		echo $(show_time $currentTime) "- Nightime"
		bash SnapShot5.sh
		sleep 39
	fi
done


