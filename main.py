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

print('Starting up...')
reboot = "LuaUPnP boot"
lastLine = ""
appendedLine= ""
vera_host = os.environ.get('VERA_HOST')
es_host = os.environ['ES_HOST']
es_port = os.environ['ES_PORT']
vera_log_index = os.environ['VERA_LOG_INDEX']
sleep_time = int(os.environ['SLEEP_TIME'])
# if os.environ.get("REBOOT_TIME"):
#     reboot_time = os.environ["REBOOT_TIME"]
#     print("Rebooting at", reboot_time)
# else:
#     reboot_time = None
startup = True
es = Elasticsearch(hosts=[{'host': es_host, 'port': es_port}])
url = "http://{}/cgi-bin/cmh/log.sh?Device=LuaUPnP".format(vera_host)
tag_line_exp = re.compile(
    r'\d{2}[\t]\d{2}[-/]\d{2}[-/]\d{2} \d{1,2}:\d{2}:\d{2}.\d{3}')
date_exp = re.compile(r'\d{2}[-/]\d{2}[-/]\d{2} \d{1,2}:\d{2}:\d{2}.\d{3}')

def compose(message, timestamp):
    doc = {
        'timestamp': convert_to_utc(timestamp),
        'message': message,
        'vera_host': os.environ.get('VERA_HOST'),
        'es_host': os.environ.get('ES_HOST'),
        'es_port': os.environ.get('ES_PORT'),
        'machine_time': datetime.now()
    }
    return doc

while True:
    response = get_from_vera(url)
    # if str(response) == "reboot":
    #     lastLine = reboot
    #     continue
    soup = BeautifulSoup(response.text, features="html.parser")
    allLines = soup.text.split('\n')
    found = -1
    start_index = 0
    lines = []
    if not startup:
        for i in range(len(allLines)-1,0,-1):
            if lastLine in allLines[i] and re.search(tag_line_exp, allLines[i]):
                start_index = i
                break
    else:
        startup = False
        start_index = 0
        doc = compose("START INDEX RESET TO 0",datetime.now())
        submit_to_es(es,doc)

    search = False
    # print("Total # of lines {}".format(len(allLines)))
    # Find the last lines we exported and start adding from there.
    for i in range(start_index, len(allLines)):
        line = allLines[i]
        if re.search(tag_line_exp, str(line)) and not appendedLine == line:
            lines.append(line)
            appendedLine = line
        else:
            print("skipped line:",line)

    # now add those lines to elastic search
    match = None
    local_time = datetime.now().replace(tzinfo=tz.tzlocal())
    print("Pushing {} lines to ES @ {}".format(len(lines), local_time), flush=True)
    if len(lines) > 0:
        for line in lines:
            theLine = str(line).split('\n')
            for aLine in theLine:
                strippedText = aLine.split('\t')
                if re.search(tag_line_exp, aLine) and len(strippedText) > 2:
                    message = BeautifulSoup(aLine, features="html.parser").text
                    timestamp = datetime.strptime(
                        re.search(date_exp, aLine).group(0),  '%m/%d/%y %H:%M:%S.%f')
                    submit_to_es(es, compose(message, timestamp))
        lastLine = aLine
    time.sleep(sleep_time)
