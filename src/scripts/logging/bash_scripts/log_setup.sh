#!/bin/bash

# Install prereqs
apt-get install gnupg
apt-get install software-properties-common
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

# Setup Rsyslog
add-apt-repository ppa:adiscon/v8-devel
apt-get update
apt-get install rsyslog
cp rsyslog.conf /etc/
cp rsyslog.d/50-default.conf /etc/rsyslog.d/
cp rsyslog.d/60-osquery.conf /etc/rsyslog.d/
chmod -R 764 /var/log
rsyslogd

# Setup OSQuery
cp osquery.conf /etc/osquery/
cp osquery.flags /etc/osquery/
cp -R packs /etc/osquery/

# Check configuration
osqueryctl config-check

# Run the OSQuery Daemon on scheduled intervals
osqueryd "--verbose"

# Logs are stored here: /var/log/osquery/osqueryd.results.log
