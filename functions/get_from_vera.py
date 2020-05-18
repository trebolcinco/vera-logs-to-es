import requests
import requests.exceptions
from requests.exceptions import ChunkedEncodingError, ConnectionError, ConnectTimeout, HTTPError
import time
from datetime import datetime
from datetime import timedelta
import os
sleep_time = int(os.environ['SLEEP_TIME'])
# reboot_time = None
# if os.environ.get('REBOOT_TIME'):
#   init_reboot_time = datetime.strptime(os.environ['REBOOT_TIME'],"%H:%M:%S")
# else:
#   init_reboot_time = None

def get_from_vera(url):
  # if init_reboot_time:
  #  reboot_time = init_reboot_time.replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)

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
        # if reboot_time:
        #   startTime  = reboot_time
        #   endTime = reboot_time + timedelta(minutes=15)
        #   now = datetime.now()
        #   if now > startTime and now < endTime:
        #     return "reboot"
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