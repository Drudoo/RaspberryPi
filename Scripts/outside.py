import urllib.request, urllib.parse, json 
import time
from datetime import datetime, timedelta

city=['2618425']
cityName=['outside']
cityTime=[0]

for index, elem in enumerate(city):
	db_data=[]
	with urllib.request.urlopen('http://192.168.0.10') as url:
		data = json.loads(url.read().decode())
		timestamp = datetime.now()
		db_data.append(('city','outside'))
		db_data.append(('temp',float(data["Temperature"]["Celsius"])))
		db_data.append(('time',timestamp.strftime('%Y-%m-%d %H:%M:%S')))
		db_data=urllib.parse.urlencode(db_data).encode("utf-8")
		path='<postURL>'    #the url you want to POST to
		req=urllib.request.Request(path, db_data)
		req.add_header("Content-type", "application/x-www-form-urlencoded")
		page=urllib.request.urlopen(req).read()




#INSERT INTO `temperature`(`city`, `temp`, `time`) VALUES ('cph',d'22.21','2018-02-05 14:46:14')
