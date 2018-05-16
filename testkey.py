#!/usr/bin/python
import RPi.GPIO as GPIO  
import csv
import datetime
import sys
import signal

GPIO.setmode(GPIO.BCM)  
  
# GPIO 23 & 17 set up as inputs, pulled up to avoid false detection.  
# Both ports are wired to connect to GND on button press.  
# So we'll be setting up falling edge detection for both  
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

with open('/home/pi/happiness.csv', 'w') as csvfile:
    fieldnames = ['timestamp', 'happiness']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

# now we'll define two threaded callback functions  
# these will run in another thread when our events are detected  
def callback_happy(channel):  
    with open('happiness.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        time = datetime.datetime.now().isoformat()
        writer.writerow([time, 'happy'])
    print "Happy pressed"  

def callback_content(channel):  
    global writer
    print "Content pressed"  
    writer.writerow({'timestamp': time.time(), 'happiness': 'content'})


def callback_sad(channel):  
    global writer
    print "Sad pressed"  
    writer.writerow({'timestamp': time.time(), 'happiness': 'sad'})

def sigterm_handler(_signo, _stack_frame):
    """When sysvinit sends the TERM signal, cleanup before exiting."""
    print("[" + datetime.datetime.now().isoformat() + "] received signal {}, exiting...".format(_signo))
    GPIO.cleanup()
    sys.exit(0)

print "Make sure you have a button connected so that when pressed"  
print "it will connect GPIO port 23 (pin 16) to GND (pin 6)\n"  
print "You will also need a second button connected so that when pressed"  
print "it will connect GPIO port 24 (pin 18) to 3V3 (pin 1)\n"  
print "You will also need a third button connected so that when pressed"  
print "it will connect GPIO port 17 (pin 11) to GND (pin 14)"  
raw_input("Press Enter when ready\n>")  
  
# Setting up signal interrupt
GPIO.add_event_detect(23, GPIO.FALLING, callback=callback_sad, bouncetime=300)  
GPIO.add_event_detect(17, GPIO.FALLING, callback=callback_content, bouncetime=300)  
GPIO.add_event_detect(24, GPIO.FALLING, callback=callback_happy, bouncetime=300)  
signal.signal(signal.SIGTERM, sigterm_handler)
  
try:  
    raw_input("Press enter to end program\n>")  
  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  