# Logging README
## OSQuery Configurations
OSQuery's FIM is handled by different services on Windows and Linux. Because of this, the configuration file varries slightly. The Packs available to Windows and Linux are also different in some ways, which has resulted in two OSQuery configuration files.
For some reason, OSQuery in a container does not like having auditing options set. This is done in the `osquery.flags` file instead
as trouble retrieving kernel files from a docker container.

## Filebeat
### Install Filebeat on Linux
- Copy the bash_scripts folder into each linux container. This and the following steps are handled by Portainer, but if manual installation is required, continue reading the next two steps.
- Make the script `log_setup_linux.sh` executable and run with `./log_setup_linux.sh`
- Ensure the logstash output "hosts" IP in filebeat.yml is correctly pointing at the logstash container

### Install Filebeat on Windows
- Install Filebeat manually through the Elastic website. Sadly, there is no other option for installing filebeat on windows
- Copy the filebeat.yml file to the installation of filebeat's data folder, typically: `C:ProgramData\Elastic\Beats\filebeat`
- Remove the reference.yml and example.yml from this folder
- Uncomment line 32: `- "c:\program files\osquery\log\osqueryd.results.log"` in the filebeat.yml configuration
- Comment out line 28 and 29 in filebeat.yml

### Running filebeat on Linux and Mac
- Filebeat service starts when the log_setup_*.sh file is run on Mac or Linux.
- This is done automatically when the Oceano stack starts in portainer

### Running filebeat on Windows
- To start filebeat in the foreground, navigate to the filebeat folder: `C:Program Files\Elastic\Beats\8.1.2\filebeat` and run the command:
`filebeat.exe -e --path.config "c:program files\elastic\beats\8.1.2\filebeat"` 
- To start filebeat as a service, in powershell, run `Start-Service filebeat`

### Issues
- Filebeat does not want to be started as a service on Windows. There is little to no useful information on this issue within the Elastic Forums. The solution that I found was ensuring that the filebeat.yml we created replaces the two example and reference yml files in `C:\ProgramData\Elastic\Beats\filebeat`
- As mentioned above, Filebeat has no installation method for Windows other than through their installer.
