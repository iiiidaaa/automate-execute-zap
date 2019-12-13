# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
import sys , json
import datetime

def sendJson(fileName):
  es = Elasticsearch("http://10.1.2.20:9200",verify_certs=False)
  today = str(datetime.date.today())
  now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat()
  try:
    with open(fileName, 'r') as f:
      data = json.load(f)
      if isinstance(data["Report"]["Sites"], list):
        for site in data["Report"]["Sites"]:
          putAlertToES(site["Alerts"]["AlertItem"],es,today,now)
      else:
        putAlertToES(data["Report"]["Sites"]["Alerts"]["AlertItem"],es,today,now)
  except json.JSONDecodeError as e:
      print('JSONDecodeError: ', e)
#  except Exception as e:
#    print("Error:")
#    print(e)

def putAlertToES(alertItem,es,today,now):
  if isinstance(alertItem, list):
    for alert in alertItem:
      sendDataToES(alert,es,today,now)
  else:
    sendDataToES(alertItem,es,today,now)

def sendDataToES(alert,es,today,now):
  alert["time"] = now
  if isinstance(alert["Item"], list):
    tmp_alert = alert
    for item in alert["Item"]:
      tmp_alert["Item"] = item
      es.index(index="test-" + today, doc_type="test", body=tmp_alert)
  else:
    es.index(index="test-" + today, doc_type="test", body=alert)

fileName = sys.argv[1]
sendJson(fileName)

