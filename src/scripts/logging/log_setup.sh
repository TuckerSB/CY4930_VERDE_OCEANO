#!/bin/bash

# Install prereqs
apt-get install gnupg
apt-get install software-properties-common
apt install linux-libc-dev
apt-get update; apt-get install curl
apt-get update

# Install OSQuery
export OSQUERY_KEY=1484120AC4E9F8A1A577AEEE97A80C63C9D8B80B
echo 'key exported'
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys $OSQUERY_KEY
add-apt-repository 'deb [arch=amd64] https://pkg.osquery.io/deb deb main'
echo 'repository added'
apt-get update
apt-get install osquery
echo 'osquery installed'

# Setup OSQuery
cp osquery.conf /etc/osquery/
cp osquery.flags /etc/osquery/
cp -R packs /etc/osquery/

# Check configurations
osqueryctl config-check

# Install Filebeat
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-oss-7.15.1-amd64.deb
dpkg -i filebeat-oss-7.15.1-amd64.deb

# Setup Filebeat
chown root:root /etc/filebeat/filebeat.yml
cp filebeat.yml /etc/filebeat/filebeat.yml
filebeat -e -c /etc/filebeat/filebeat.yml

# Run the OSQuery Daemon on scheduled intervals
osqueryd

# Run Filebeat
./bin/filebeat -e

# Logs are stored on each machine locally: /var/log/osquery/osqueryd.results.log
