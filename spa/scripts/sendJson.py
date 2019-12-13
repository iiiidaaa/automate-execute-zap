# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
import sys , json
import datetime

def sendJson(fileName,index):
  es = Elasticsearch("http://10.1.2.20",verify_certs=False)
  today = str(datetime.date.today())
  now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat()
  try:
    with open(fileName, 'r') as f:
      data = json.load(f)
      if isinstance(data["Report"]["Sites"], list):
        for site in data["Report"]["Sites"]:
          putAlertToES(site["Alerts"]["AlertItem"],es,today,now,index)
      else:
        putAlertToES(data["Report"]["Sites"]["Alerts"]["AlertItem"],es,today,now,index)
  except json.JSONDecodeError as e:
      print('JSONDecodeError: ', e)
#  except Exception as e:
#    print("Error:")
#    print(e)

def putAlertToES(alertItem,es,today,now,index):
  if isinstance(alertItem, list):
    for alert in alertItem:
      sendDataToES(alert,es,today,now,index)
  else:
    sendDataToES(alertItem,es,today,now,index)

def sendDataToES(alert,es,today,now,index):
  alert["time"] = now
  if isinstance(alert["Item"], list):
    tmp_alert = alert
    for item in alert["Item"]:
      tmp_alert["Item"] = item
      es.index(index=index + "-" + today, doc_type=index, body=tmp_alert)
  else:
    es.index(index=index + "-" + today, doc_type=index, body=alert)