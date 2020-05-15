import elasticsearch
import time
import os
sleep_time = int(os.environ['SLEEP_TIME'])

def submit_to_es(es, doc):

    while True:
        try:
            res = es.index(index="vera-log", body=doc)
            return 0
        except Exception as ex:
            print("ES failed, retrying forever:", repr(ex))
            time.sleep(sleep_time)
            continue