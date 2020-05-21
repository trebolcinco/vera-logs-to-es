import elasticsearch
import time
import os
sleep_time = int(os.environ['SLEEP_TIME'])
vera_log_index = os.environ["VERA_LOG_INDEX"]

def submit_to_es(es, doc):

    while True:
        try:
            res = es.index(index=vera_log_index, body=doc)
            return 0
        except Exception as ex:
            print("ES failed, retrying forever:", repr(ex))
            time.sleep(sleep_time)
            continue