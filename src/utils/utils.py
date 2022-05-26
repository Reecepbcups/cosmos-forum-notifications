import datetime
import requests
import urllib.parse

def getISO8601Time(encode=True):
    output = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z"
    if encode: output = output.replace(":", "%3A")
    return output

def getTopicList(url, key="topic_list") -> dict:
    response = requests.get(url)
    data = response.json()
    if key in data:
        data = data[key]
    return data

epoch = datetime.datetime(1970, 1, 1)
def getEpochTime(createTime) -> int:
    current = datetime.datetime.strptime(createTime, "%Y-%m-%dT%H:%M:%S.%fZ")
    return int((current - epoch).total_seconds())

def unecode_text(msg):
    return urllib.parse.unquote(msg)