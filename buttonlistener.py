#!/usr/bin/python
import RPi.GPIO as GPIO
import datetime
import sys
import signal
import MySQLdb
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

GPIO.setmode(GPIO.BCM)
PORT = 8088

# GPIO 17, 23, 24 set up as inputs, pulled up to avoid false detection.
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def writetodb(happiness):
    query = "INSERT INTO happy(happiness,timestamp) " \
                "VALUES(%s,%s)"
    args = (happiness, datetime.datetime.now())

    try:
        conn = MySQLdb.connect(host="",port=3306,user="",passwd="",db="")
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
        log(happiness + " pressed")
    except:
        log("Couldn't add to database")

    finally:
        cursor.close()
        conn.close()

def log(mess):
    print(str(datetime.datetime.now()) + ": " + mess)

def callback_happy(channel):
    writetodb('happy')

def callback_content(channel):
    writetodb('content')

def callback_sad(channel):
    writetodb('sad')

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