import json
from pprint import pprint
import threading
import time 

import datetime
import schedule

import colorsys
try:
    import unicornhat
except ImportError:
    print('The unicornhat package needs to be installed !')
    try:
        from LightUpHardware import unicornhatmock as unicornhat
    except ImportError:
        import unicornhatmock as unicornhat
    unicornhat.verbose = False
    print('Mock unicornhat module imported.')


alarmOn = False;
brightness_start = 0.3
brightness_end = 0.5

def gradual_light_on(seconds):
    global alarmOn
    sleep_time = seconds / 200.0
    brightness_step = (brightness_end - brightness_start) / 200.0
    brightness_level = brightness_start

    # Set all the pixels to the yellowish colour
    r, g, b = colorsys.hsv_to_rgb(0.108, 0.6, 1.0)
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    for y in range(8):
        for x in range(8):
            unicornhat.set_pixel(x, y, r, g, b)
    unicornhat.brightness(brightness_start)
    unicornhat.show()
    # Increase brightness gradually
    while brightness_level < brightness_end:
        unicornhat.brightness(brightness_level)
        unicornhat.show()
        brightness_level += brightness_step
        time.sleep(sleep_time)
    unicornhat.clear()
    unicornhat.show()
    alarmOn = False;

def printit():
    global alarmOn
    now = datetime.datetime.now().strftime('%-H:%-M')
    date = datetime.datetime.now()
    with open('/home/pi/www/html/Alarm/alarms.json') as data_file:    
        data = json.load(data_file)
        for x in data:
            time = str(x['time']['hours'])+":"+str(x['time']['minutes']);
            print x['enabled'],date.strftime('%a'),time,now
            for y in x['days']:
                for key in y.keys():
                    if y[key]==True and key==date.strftime('%a'):
                        if time==now and not alarmOn and x['enabled']:
                            print "The ",time,"alarm is going off"
                            alarmOn = True;
                            gradual_light_on(1800)
                
        #print "Set an alarm called ",x['id']," for ", time," every ",x['days']
        print

schedule.every(1).minutes.do(printit)



def showAlarm():
    global alarmOn
    x=10
    while x > 0:
        print x
        x-=1
        time.sleep(1)
    alarmOn = False;

    
while True:
    schedule.run_pending()
    time.sleep(1)
