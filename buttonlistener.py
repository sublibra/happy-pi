#!/usr/bin/python
import RPi.GPIO as GPIO
import datetime
import sys
import signal
import requests
import time

GPIO.setmode(GPIO.BCM)
URL = "http://[SERVER]/add/mood/"

# GPIO 17, 23, 24 set up as inputs, pulled up to avoid false detection.
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def reportHappiness(happiness):
    print (happiness + " pressed")
    headers = {"Content-Type": "application/json"}
    req = None
    try:
        req = requests.put(url + happiness, headers=headers)
        log(happiness + " pressed")
    except:
        if req != None:
            log("Couldn't add to database")

def log(mess):
    print(str(datetime.datetime.now()) + ": " + mess)

def callback_happy(channel):
    reportHappiness('happy')

def callback_content(channel):
    reportHappiness('content')

def callback_sad(channel):
    reportHappiness('sad')

def sigterm_handler(_signo, _stack_frame):
    """When sysvinit sends the TERM signal, cleanup before exiting."""
    print(datetime.datetime.now() + ": received signal {}, exiting...".format(_signo))
    GPIO.cleanup()
    sys.exit(0)

# Attach event handlers to events
GPIO.add_event_detect(17, GPIO.FALLING, callback=callback_content, bouncetime=1000)
GPIO.add_event_detect(23, GPIO.FALLING, callback=callback_sad, bouncetime=1000)
GPIO.add_event_detect(24, GPIO.FALLING, callback=callback_happy, bouncetime=1000)
signal.signal(signal.SIGTERM, sigterm_handler)

log("Starting Happy-pi button listener.")
while True:
    time.sleep(1e6)

GPIO.cleanup()           # clean up GPIO on normal exit