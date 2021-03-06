# Vera-Logs-To-ES
Scrapes vera logs from the hubs http endpoint and then pushes them to Elastic Search.

## Elastic Search
- Vera-Logs-To_ES will automatically create the log index and policy for you, if you want a different policy fork and update.

- A timestamp is required, only Vera log lines that include a timestamp will be pushed to ES.

## Variables
Following varaibles need to be set:

<pre>
1. ES_HOST="0.0.0.0"
2. ES_PORT="0000"
3. VERA_HOST="0.0.0.0"         (IP of your vera hub)
</pre>
These variables are defaulted but can be overridden.
<pre>
1. VERA_LOG_INDEX="vera-log"   (Name of index to create in ES)
2. PYTHONUNBUFFERED=1          (Docker Only)
3. SLEEP_TIME=60               (How much time to sleep between log calls)
4. SKIP_RELOAD="false"         (Replace index, policy and template at startup"
</pre>

## Notes
<pre>
1. SKIP_RELOAD - Reload is neccessary due to Docker resetting a container and then on restart the app would reread log from start and duplicates happen.
2. Log Levels
 Log levels for data sent to the Z-Wave dongle:
      01 = critical errors
      02 = warnings
      03 = start/stop/reload events
      04 = jobs
      05 = warnings
      06 = variables (which indicates state changes)
      07 = events
      08 = commands
      10 = status messages
      41 = data sent to the Z-Wave dongle
      42 = data received from the Z-Wave dongle
      50 = luup log
</pre?>
## What's Missing
- Not support for a username/password for Elastic Search
- Tests

