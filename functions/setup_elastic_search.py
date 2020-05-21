import json
import requests
import requests.exceptions
import os
from requests.exceptions import ChunkedEncodingError, ConnectionError, ConnectTimeout, HTTPError
vera_log_index = os.environ["VERA_LOG_INDEX"]
headers = {"Content-Type":"application/json"}

def reload_es(url):
  with open("./elastic-search/vera-log-mapping.json") as mapping_file:
    mapping = json.load(mapping_file)
  with open("./elastic-search/vera-log-policy.json") as policy_file:
    policy = json.load(policy_file)
  with open("./elastic-search/vera-log-template.json") as template_file:
    template = json.load(template_file)

  es_delete(url)
  es_policy(url, policy)
  es_template(url, template)
  es_mapping(url, mapping)

def es_mapping(url, mapping):
  try:
    response = requests.put(url+"/{}-000001".format(vera_log_index), data=json.dumps(mapping), headers=headers )
    response.raise_for_status()
  except Exception as ex:
    print("Policy Exception:",ex)
    raise

def es_template(url, template):
  try:
    response = requests.put(url+"/_template/vera-log_template", data=json.dumps(template), headers=headers )
    response.raise_for_status()
  except Exception as ex:
    print("Policy Exception:",ex)
    raise

def es_policy(url, policy):
  try:
    response = requests.put(url+"/_ilm/policy/vera-log_policy", data=json.dumps(policy), headers=headers )
    response.raise_for_status()
  except Exception as ex:
    print("Policy Exception:",ex)
    raise

def es_delete(url):
  try:
    response = requests.delete(url+"/{}*".format(vera_log_index))
    response.raise_for_status()
  except Exception as ex:
    print("Delete Exception:",ex)
    raise
