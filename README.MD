# Vera-Logs-To-ES
Scrapes vera logs from the hubs http endpoint and then pushes them to Elastic Search.

## Elastic Search
- See the files in the elastic-search folder, you can use the example shell script to install your index but you'll need to set the ip.

- A timestamp is required, it will be set to the logs timestamp.

## Variables
Following varaibles need to be set:

1. ES_HOST="0.0.0.0"
2. ES_PORT="0000"
3. VERA_HOST="0.0.0.0"         (IP of your vera hub)

These variables are defaulted but can be overridden.

1. VERA_LOG_INDEX="vera-log"   (Name of index to create in ES)
2. PYTHONUNBUFFERED=1          (Docker Only)
3. SLEEP_TIME=60               (How much time to sleep between log calls)
4. REBOOT_TIME="03:00:00"      (If you do a nightly reboot then what time is that? Allows us    to not add duplicate log info after the reboot).  **If you don't do a scheduled reboot then do not set reboot time (e.g, REBOOT_TIME=).**

## What's Missing
- Not support for a username/password for Elastic Search
- Tests