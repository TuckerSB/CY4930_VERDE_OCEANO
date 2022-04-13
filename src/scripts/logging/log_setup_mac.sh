#!/bin/bash

# Install Filebeat
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.1.2-darwin-x86_64.tar.gz
tar xzvf filebeat-8.1.2-darwin-x86_64.tar.gz

# Setup Filebeat - This is not a guaranteed location (I don't have a MAC to test this with)
chown root:root /etc/filebeat/filebeat.yml
cp filebeat.yml /etc/filebeat/filebeat.yml

# Test the Filebeat config file
./filebeat -e -c filebeat.yml

# Run Filebeat - May need to be modified for correct location
./bin/filebeat -e