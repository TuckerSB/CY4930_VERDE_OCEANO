#!/bin/bash

# Install prereqs
apt-get install gnupg
apt-get install software-properties-common
apt install linux-libc-dev
apt-get update; apt-get install curl
apt-get update

# Install Filebeat
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-oss-7.15.1-amd64.deb
dpkg -i filebeat-oss-7.15.1-amd64.deb

# Setup Filebeat
chown root:root /etc/filebeat/filebeat.yml
cp filebeat.yml /etc/filebeat/filebeat.yml
filebeat -e -c /etc/filebeat/filebeat.yml

# Run Filebeat
./bin/filebeat -e
