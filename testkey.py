#!/usr/bin/python
import RPi.GPIO as GPIO  
import csv
import datetime
import sys
import signal
import SimpleHTTPServer
import SocketServer
import requests
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

GPIO.setmode(GPIO.BCM)  
PORT = 8088
DESTFILE = '/home/pi/happiness.csv'
EVENT_TARGET = ""

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

def emitEvent():
    global EVENT_TARGET
    if EVENT_TARGET == "":
        print("EVENT TARGET NOT SET")
    else:   
        print("Sending event to:" + EVENT_TARGET)
        requests.head(EVENT_TARGET, timeout=0.1)        

def callback_happy(channel):  
    with open(DESTFILE, 'a') as csvfile:
        writer = csv.writer(csvfile)
        time = datetime.datetime.now().isoformat()
        writer.writerow([time, 'happy'])
    emitEvent()
    print "Happy pressed"  

def callback_content(channel):  
    with open(DESTFILE, 'a') as csvfile:
        writer = csv.writer(csvfile)
        time = datetime.datetime.now().isoformat()
        writer.writerow([time, 'content'])
    emitEvent()
    print "Content pressed"  

def callback_sad(channel):  
    with open(DESTFILE, 'a') as csvfile:
        writer = csv.writer(csvfile)
        time = datetime.datetime.now().isoformat()
        writer.writerow([time, 'sad'])
    emitEvent()
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
class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def do_GET(self):
        f = open(DESTFILE, 'rb') 
        self.send_response(200)
        self.send_header('Content-type',    'text/csv')
        self.end_headers()
        self.wfile.write(f.read())
        f.close()
    def do_POST(self):
        global EVENT_TARGET
        self._set_headers()
        EVENT_TARGET = "http://{}:{}".format(self.client_address[0], PORT)
        body = "<html><body><h1>WOHO</h1>I will happily emit events to you on:"
        body += EVENT_TARGET + "</body></html>"
        print(body)
        self.wfile.write(body)

def run(server_class=HTTPServer, handler_class=RequestHandler, port=PORT):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Happy server running localhost:{}'.format(PORT)
    httpd.serve_forever()

run()
GPIO.cleanup()           # clean up GPIO on normal exit  