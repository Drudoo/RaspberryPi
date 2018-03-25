#!/bin/bash
#temp=$(curl -s '192.168.0.10' | jq -r .Temperature.Celsius | sed 's/\\[tn]//g')

city=('2618425' '5206379' '4815352' '4167147') #
cityName=('copenhagen' 'pittsburgh' 'morgantown' 'orlando')
cityTime=(0 -6 -6 -6)

for i in ${!city[@]}; do
	url="http://api.openweathermap.org/data/2.5/weather?id="${city[$i]}"&APPID=<APIKEY>&units=metric"
	temp=$(curl -s $url | jq -r .main.temp | sed 's/\\[tn]//g')
	udate=$(date +%s)
	uzone=${cityTime[$i]}
	utime="$((($udate+($uzone*3600))*1000000000))"
	echo ${city[$1]} $temp $utime
	curl -XPOST "localhost:8086/write?db=temperature" --data-binary "${cityName[$i]},host=OpenWeatherMap value=${temp} $utime"
done
#temp=$(curl -s '192.168.0.10' | jq -r .Temperature.Celsius | sed 's/\\[tn]//g; s/[[:blank:]]//g')
#udate=$(date +%s)
#uzone=${cityTime[0]}
#utime="$((($udate+($uzone*3600))*1000000000))"
#curl -XPOST "http://localhost:8086/write?db=temperature" --data-binary "outside,host=BedroomWemos2 value=${temp} $utime"
#echo "outside" $temp $utime

#curl -XPOST "http://localhost:8086/write?db=temperature" --data-binary "outside,host=BedroomWemos2 value=${temp}"


#1518801072785348921
