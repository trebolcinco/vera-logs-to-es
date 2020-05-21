import requests
import requests.exceptions
from requests.exceptions import ChunkedEncodingError, ConnectionError, ConnectTimeout, HTTPError
import time
from datetime import datetime
from datetime import timedelta
import os
sleep_time = int(os.environ['SLEEP_TIME'])

def get_from_vera(url):

  while True:
    try:
        response = requests.get(url)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except requests.exceptions.ChunkedEncodingError as errch:
        print("Chunked Error", errch)
        time.sleep(sleep_time)
        continue
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        time.sleep(sleep_time)
        continue
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        time.sleep(sleep_time)
        continue
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
        time.sleep(sleep_time)
        continue
    except requests.exceptions.RequestException as err:
        print("Request Exception:", err)
        time.sleep(sleep_time)
        continue
    except Exception as ex:
        print("General Exception:", ex)
        raise
    return response