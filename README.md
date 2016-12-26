# monitor info
Name:system-info monitor
Version:1.0.0
Copyright: Meng Chen 369575409@qq.com

# Before run
centos 7 + python2.7 + psutils
Use dockerfile to create image

# How to run
docker run -t -i  --restart=always --net=host -e="SERVER_ADDRESS=host:port" --name="systemmonitor" imageID /bin/bash -c "cd root/sysinfo_monitor/;python main.py "

# After run
Need a terminal to collect udp(gelf type) infomation
