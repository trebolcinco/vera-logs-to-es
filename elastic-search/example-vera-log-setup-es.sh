#!/bin/bash
# Setups up ES index with mappings, policy and template
curl -X DELETE http://{ip}:9200/vera-log*
curl -X PUT -H "Content-Type: application/json" -d @vera-log-policy.json 'http://{ip}}:9200/_ilm/policy/vera-log_policy'
curl -X PUT -H "Content-Type: application/json" -d @vera-log-template.json 'http://{ip}}:9200/_template/vera-log_template'
curl -X PUT -H "Content-Type: application/json" -d @vera-log-mapping.json 'http://{ip}:9200/vera-log-000001'
curl -X GET http://{ip}:9200/vera-log
