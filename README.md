# monitor
system-info monitor

# How to run
docker run -t -i  --restart=always --net=host -e="SERVER_ADDRESS=host:port" --name="systemmonitor" imageID /bin/bash -c "cd root/sysinfo_monitor/;python main.py "

# Before run
centos 7 + python2.7 + psutils
