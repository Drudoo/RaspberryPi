import urllib.request, urllib.parse, json 
import time
from datetime import datetime, timedelta

city=['2618425','5206379','4815352','4167147']
cityName=['copenhagen','pittsburgh','morgantown','orlando']
cityTime=[0,-6,-6,-6]

for index, elem in enumerate(city):
	db_data=[]
	with urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?id='+elem+'&APPID=<APIKEY>&units=metric') as url:
		data = json.loads(url.read().decode())
		timestamp = datetime.now() + timedelta(hours=cityTime[index])
		db_data.append(('city',cityName[index]))
		db_data.append(('temp',float(data["main"]["temp"])))
		db_data.append(('time',timestamp.strftime('%Y-%m-%d %H:%M:%S')))
		db_data=urllib.parse.urlencode(db_data).encode("utf-8")
		path='<POST URL>'    #the url you want to POST to
		req=urllib.request.Request(path, db_data)
		req.add_header("Content-type", "application/x-www-form-urlencoded")
		page=urllib.request.urlopen(req).read()




#INSERT INTO `temperature`(`city`, `temp`, `time`) VALUES ('cph',d'22.21','2018-02-05 14:46:14')
