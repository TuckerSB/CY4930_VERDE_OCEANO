# CY4930_VERDE_OCEANO
## Team Verde:
- Christian Like
- Mark Latuhkin
- Tucker Brouillard
- Walker Lambrecht
## Project Oceano:
1. Stand up a mock netowrk
    1. 5 Linux Containers
    2. 1 Windows Virtual Machine
    3. 1 Mac Laptop
    4. 1 Apache Web Server
    5. 1 MySQL Database
    6. 1 Linux Bind DNS Server
2. Stand up a logging solution
    1. ELK Stack to ingest, store, and view log files
    2. OSQuery to generate logs
    3. FleetDM to manage endpoints and remote queries
    4. Filebeat to retrieve logs from endpoints
3. Identify suspicious activity
    1. Simulate malicious activity
    2. Parse activity into logs
    3. Alert when activity is detected
## Files
- src - All project files
    - ELK - The ELK stack code and configurations running s the logging solution
        - /logstash/pipeline/logstash.conf - The Logstash configuration 
    - EndpointScripts - Scripts for enrolling endpoints with FleetDM
    - scripts - Scripts for generating and detecting activity
        - Attacks - Ransomware, Registry Editing, and Syn Flood activity scripts
        - ELK - Early sample JSON logs and their mapping
        - file_events - Scripts for generating random file events and simple web traffic in bulk
        - logging - Scripts for filebeat setup and Syn Flood detection
     - WWW - The web server code
