# Logging README
## OSQuery
### Install
- Copy the bash_scripts folder into each linux container
- Make the script `log_setup.sh` executable and run with `./log_setup.sh`

### TODO:
- Setup FIM for OSQuery with an FIM configuration file as well.
- Automated enrollment of client in FleetDM

### Issues
- For some reason, OSQuery in a container does not like having auditing options set. This is done in the `osquery.flags` file instead
as trouble retrieving kernel files from a docker container.