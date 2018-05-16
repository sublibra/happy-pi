#!/usr/bin/python
import RPi.GPIO as GPIO  
import csv
import datetime
import sys
import signal
import SimpleHTTPServer
import SocketServer

GPIO.setmode(GPIO.BCM)  
PORT = 666
DESTFILE = '/home/pi/happiness.csv'
  
# GPIO 17, 23, 24 set up as inputs, pulled up to avoid false detection.  
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

with open(DESTFILE, 'r') as csvfile:
    csv_dict = [row for row in csv.DictReader(csvfile)]
    if len(csv_dict) == 0:
        print('csv file is empty, add headers')
        with open(DESTFILE, 'w') as csvfile:
            fieldnames = ['timestamp', 'happiness']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

def callback_happy(channel):  
    with open(DESTFILE, 'a') as csvfile:
        writer = csv.writer(csvfile)
        time = datetime.datetime.now().isoformat()
        writer.writerow([time, 'happy'])
    print "Happy pressed"  

def callback_content(channel):  
    with open(DESTFILE, 'a') as csvfile:
        writer = csv.writer(csvfile)
        time = datetime.datetime.now().isoformat()
        writer.writerow([time, 'content'])
    print "Content pressed"  

def callback_sad(channel):  
    with open(DESTFILE, 'a') as csvfile:
        writer = csv.writer(csvfile)
        time = datetime.datetime.now().isoformat()
        writer.writerow([time, 'sad'])
    print "Sad pressed"  

def sigterm_handler(_signo, _stack_frame):
    """When sysvinit sends the TERM signal, cleanup before exiting."""
    print("[" + datetime.datetime.now().isoformat() + "] received signal {}, exiting...".format(_signo))
    GPIO.cleanup()
    sys.exit(0)

# Attach event handlers to events  
GPIO.add_event_detect(17, GPIO.FALLING, callback=callback_content, bouncetime=300)  
GPIO.add_event_detect(23, GPIO.FALLING, callback=callback_sad, bouncetime=300)  
GPIO.add_event_detect(24, GPIO.FALLING, callback=callback_happy, bouncetime=300)  
signal.signal(signal.SIGTERM, sigterm_handler)

# Setup web server serving the resulting files (and more)
# In future ensure only the csv file can be served
Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)
try:  
    print "Serving files at:", PORT
    httpd.serve_forever()
  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  