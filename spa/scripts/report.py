import requests
import datetime
from pprint import pprint

def CreateReport(conf,path):

    # Setting
    today = str(datetime.date.today())
    infoList = [
    "Vulnerability Report", # title
    "Automatic Scan",       # by
    "Someone",              # for
    today,                  # scan Date
    today,                  # reportDate
    "test",                 # scanVer
    "test",                 # reportVer
    "test" ]                # description

    url = "http://" + conf.proxyAddr + "/JSON/exportreport/action/generate/"
    # POSTData
    apiKey = conf.apiKey
    sourceInfo = ';'.join(infoList)
    fType = "json"
    alertSeverity = "t;t;t;t"
    alertDetails = "t;t;t;t;t;t;f;f;f;f"

    try:
        response = requests.post(url,{
            'apikey' : apiKey,
            'absolutePath' : path,
            'fileExtension' : fType,
            'sourceDetails' : sourceInfo,
            'alertSeverity' : alertSeverity,
            'alertDetails' : alertDetails
        })
    except Exception as ex:
        pprint(ex)
        return False
    return response.json().get("Result") == "OK"
