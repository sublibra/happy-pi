#!/usr/bin/python
import RPi.GPIO as GPIO  
import datetime
import requests

url = "http://[SERVER]/add/mood/"

GPIO.setmode(GPIO.BCM)  
  
# # GPIO 17, 23, 24 set up as inputs, pulled up to avoid false detection.  
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

def reportHappiness(happiness):
    print (happiness + " pressed")
    headers = {"Content-Type": "application/json"}

    req = None
    try:
        req = requests.put(url + happiness, headers=headers)
    except requests.exceptions.RequestException as e:
        if req != None:
            print(req.text)
        print(e)

def callback_happy(channel):  
    reportHappiness('happy')

def callback_content(channel):  
    reportHappiness('content')

def callback_sad(channel):  
    reportHappiness('sad')

print ("Waiting for happiness!")

GPIO.add_event_detect(17, GPIO.FALLING, callback=callback_content, bouncetime=300)  
GPIO.add_event_detect(23, GPIO.FALLING, callback=callback_sad, bouncetime=300)  
GPIO.add_event_detect(24, GPIO.FALLING, callback=callback_happy, bouncetime=300)  
  
try:  
    input("Press enter to end program\n")    
  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  