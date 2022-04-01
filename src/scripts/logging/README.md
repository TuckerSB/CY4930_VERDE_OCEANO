# Logging README
## OSQuery
### Install
- Copy the bash_scripts folder into each linux container
- Make the script `log_setup.sh` executable and run with `./log_setup.sh`
- Ensure the logstash output "hosts" IP in filebeat.yml is correctly pointing at the logstash container

### TODO:
- Change config setup to run through FleetDM rather than shell script
- Remove OSQuery setup from shell script once the above is complete

### Issues
- For some reason, OSQuery in a container does not like having auditing options set. This is done in the `osquery.flags` file instead
as trouble retrieving kernel files from a docker container.
