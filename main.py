import sys
import re
import time
import datetime
import elasticsearch
import os
from elasticsearch7 import Elasticsearch
from dateutil import tz
from datetime import datetime
from bs4 import BeautifulSoup
from functions.get_from_vera import get_from_vera
from functions.push_to_elastic import submit_to_es
from functions.convert_to_utc import convert_to_utc
from functions.setup_elastic_search import reload_es

print('Starting up...')

reboot = "LuaUPnP boot"
lastLine = ""
appendedLine = ""
vera_host = os.environ.get('VERA_HOST')
es_host = os.environ['ES_HOST']
es_port = os.environ['ES_PORT']
vera_log_index = os.environ['VERA_LOG_INDEX']
sleep_time = int(os.environ['SLEEP_TIME'])
skip_reload = os.environ['SKIP_RELOAD'] == "true"
startup = True

es = Elasticsearch(hosts=[{'host': es_host, 'port': es_port}])
url = "http://{}/cgi-bin/cmh/log.sh?Device=LuaUPnP".format(vera_host)
es_base_url = "http://{}:{}".format(es_host, es_port)
tag_line_exp = re.compile(
    r'\d{2}[\t]\d{2}[-/]\d{2}[-/]\d{2} \d{1,2}:\d{2}:\d{2}.\d{3}')
date_exp = re.compile(r'\d{2}[-/]\d{2}[-/]\d{2} \d{1,2}:\d{2}:\d{2}.\d{3}')
index_tag = re.compile(r'^<.{10}>$')

if not skip_reload:
    reload_es(es_base_url)
    print("Elastic Search index {} has been deleted and reset...".format(vera_log_index))

def compose(message, timestamp, log_level):
    doc = {
        'timestamp': convert_to_utc(timestamp),
        'message': message,
        'vera_host': vera_host,
        'es_host': es_host,
        'es_port': es_port,
        'machine_time': datetime.now(),
        'log_level': log_level
    }
    return doc


last_line_count = 0
while True:
    response = get_from_vera(url)

    ## BeautifulSoup is supposed to remove all HTML using text but many spans were left over, call again seems to resolve
    old_soup = BeautifulSoup(response.text, features="html.parser")
    soup = BeautifulSoup(old_soup.text, features="html.parser")
    allLines = soup.text.split('\n')

    if last_line_count <= len(allLines):
        start_index = last_line_count
    else:
        start_index = 0
    last_line_count = len(allLines)

    lines = []
    print('DEBUG: start index == {} and last_line_count = {}'.format(
        start_index, last_line_count))

    for i in range(start_index, len(allLines)):
        line = allLines[i]
        if re.search(tag_line_exp, str(line)) and not appendedLine == line:
            lines.append(line)
            appendedLine = line

    if len(lines) > 0:
        line_count = 0
        for line in lines:
            theLine = str(line).split('\n')
            for aLine in theLine:
                strippedText = aLine.split('\t')
                if re.search(tag_line_exp, aLine) and len(strippedText) > 2:
                    message = BeautifulSoup(
                        strippedText[2], features="html.parser").text

                    if re.search(index_tag, message.strip()) or message.strip() == "":
                        # print("Skipping message, s/b tag only = ",message.strip())
                        # if the message is just a <0x12345678> tag then skip it
                        continue

                    log_level = BeautifulSoup(
                        strippedText[0], features="html.parser").text

                    timestamp = datetime.strptime(
                        re.search(date_exp, aLine).group(0),  '%m/%d/%y %H:%M:%S.%f')
                    submit_to_es(es, compose(message, timestamp, log_level))
                    line_count = line_count + 1
        lastLine = aLine
        local_time = datetime.now().replace(tzinfo=tz.tzlocal())
        push_message = "Sent {} log lines to ES @ {}".format(len(lines), local_time)
        submit_to_es(es, compose(push_message, datetime.now(),"10"))
    time.sleep(sleep_time)

# Log levels for data sent to the Z-Wave dongle:
# 01 = critical errors
# 02 = warnings
# 03 = start/stop/reload events
# 04 = jobs
# 05 = warnings
# 06 = variables (which indicates state changes)
# 07 = events
# 08 = commands
# 10 = status messages
# 41 = data sent to the Z-Wave dongle
# 42 = data received from the Z-Wave dongle
# 50 = luup log