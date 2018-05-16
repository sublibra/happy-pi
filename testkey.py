#!/usr/bin/python
import RPi.GPIO as GPIO  
import csv
import datetime
import sys
import signal

GPIO.setmode(GPIO.BCM)  
  
# GPIO 17, 23, 24 set up as inputs, pulled up to avoid false detection.  
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

with open('happiness.csv', 'r') as csvfile:
    csv_dict = [row for row in csv.DictReader(csvfile)]
    if len(csv_dict) == 0:
        print('csv file is empty, add headers')
        with open('happiness.csv', 'w') as csvfile:
            fieldnames = ['timestamp', 'happiness']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

def callback_happy(channel):  
    with open('happiness.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        time = datetime.datetime.now().isoformat()
        writer.writerow([time, 'happy'])
    print "Happy pressed"  

def callback_content(channel):  
    with open('happiness.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        time = datetime.datetime.now().isoformat()
        writer.writerow([time, 'content'])
    print "Content pressed"  

def callback_sad(channel):  
    with open('happiness.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        time = datetime.datetime.now().isoformat()
        writer.writerow([time, 'sad'])
    print "Sad pressed"  

def sigterm_handler(_signo, _stack_frame):
    """When sysvinit sends the TERM signal, cleanup before exiting."""
    print("[" + datetime.datetime.now().isoformat() + "] received signal {}, exiting...".format(_signo))
    GPIO.cleanup()
    sys.exit(0)

  
GPIO.add_event_detect(17, GPIO.FALLING, callback=callback_content, bouncetime=300)  
GPIO.add_event_detect(23, GPIO.FALLING, callback=callback_sad, bouncetime=300)  
GPIO.add_event_detect(24, GPIO.FALLING, callback=callback_happy, bouncetime=300)  
signal.signal(signal.SIGTERM, sigterm_handler)
  
try:  
    raw_input("Press enter to end program\n")  
  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  