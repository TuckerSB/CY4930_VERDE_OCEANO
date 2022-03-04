# Logging README
## OSQuery
### Install
- Copy the bash_scripts folder into each linux container
- Make the script `log_setup.sh` executable and run with `./log_setup.sh`

### Issues
- For some reason, OSQuery in a container does not like having auditing options set. This is done in the `osquery.flags` file instead

## Rsyslog Server
### Install
- Rsyslog server's Dockerfile exists in this directory. Run `docker build mysyslog .` and then follow the steps here: https://itnext.io/dockerize-rsyslog-server-f8f9754c37d5

## Rsyslog Clients
### Install
- Rsyslog client will be installed on all containers when the log_setup.sh script is run
- If the IP address of the Rsyslog server ever changes, this must be altered manually (or in the script, and run again)
    - To do so, change the IP Address in each container at the top of the file /etc/rsyslog.conf to match that of the Rsyslog server

### Issues
1. Rsyslog typically utilizes systemctl. Since Containers run on PID 1 and do not utilize Systemd, this is not available. To fix this, rsyslog's daemon is run instead
2. Rsyslog has trouble retrieving kernel files from a docker container. For this reason the kernel line in the rsyslog.conf file was removed.