# happy-pi

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
