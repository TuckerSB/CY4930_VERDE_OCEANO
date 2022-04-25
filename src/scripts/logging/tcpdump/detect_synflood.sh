#!/bin/bash
apt install net-tools
while true
do
    SYN_RECV=$(netstat -npt | awk '{print $6}' | sort | uniq -c | sort -nr | head | grep "SYN_RECV" | grep -o -E "[0-9]+")
    echo "{\"name\":\"network_connections\",\"SYN_RECV\":$SYN_RECV}" >> /var/log/network_connections.json
    sleep 60
done