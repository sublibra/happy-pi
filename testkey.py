#!/usr/bin/env python2.7  
import RPi.GPIO as GPIO  
import csv
import datetime


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
  
print "Waiting for happiness!"  
  
GPIO.add_event_detect(17, GPIO.FALLING, callback=callback_content, bouncetime=300)  
GPIO.add_event_detect(23, GPIO.FALLING, callback=callback_sad, bouncetime=300)  
GPIO.add_event_detect(24, GPIO.FALLING, callback=callback_happy, bouncetime=300)  
  
try:  
    raw_input("Press enter to end program\n")  
  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  