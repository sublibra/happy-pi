# happy-pi
A hackaton project with focus on getting a Raspberry PI geared up with physical buttons
representing the happiness level of the user. The keys represent happy, content, sad and will
when pressed store their happiness level together with a timestamp. Optionally it is also 
possible to send an event to a separate web server to pick up the latest results (download
the CSV file) and use the result. 

This is utilized in the second part of the hackaton project [happy-web](https://github.com/JohanBjerning/happy-web)

# System overview
* testkey.py - Listen to HW key events from the buttons, starts a webserver serving the CSV file, 
listens to emit event configuration, emits events through HTTP HEAD
* happy-pi - Linux run-level script ensuring the service is up and running after restart

# Usage
* Install the scripts
* Start testkey.py service
* Start hitting the keys
A file happiness.csv will be created and all new key pressed are appended to the file

* (Optionally) Send a post event to the Raspberry on port 8088 in order to setup the emit event destination
* (Optionally) Start a server listening to events on the receiver computer [happy-receiver](https://github.com/JohanBjerning/happy-web/blob/master/happy-receiver.py)
The happy-receiver.py script will receive events as soon as a button is pressed and retreive the updated
happiness.csv file

# setup
## testkey.py ##
Requires the python module requests. Install by:
```
sudo pip install requests
```

## happy-pi ##
The happy.pi init script will run the happy-py keylogger at runtime 2-5 (normal multiuser environment). Logs will be passed to /var/log and a pid file (/var/run) will be setup to ensure we only have one instance running.

### installation ###
The file is installed by calling 
```
sudo cp happy-pi /etc/init.d/
sudo chmod +x /etc/init.d/happy-pi
sudo update-rc.d happy.pi defaults
```

### usage ###
The script can be manually started/stopped through 
```
sudo service happy-pi start
sudo service happy-pi stop
```
