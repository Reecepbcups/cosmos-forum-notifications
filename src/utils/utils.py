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

def getCosmosUserMap(url) -> dict:
    '''
    Get a dict of userID to userName for cosmos hub proposals.
    '''
    tempUsers = getTopicList(url, key="users") # reuse this requests code
    users = {}
    for u in tempUsers:
        # could also save trust_level - https://forum.cosmos.network/c/hub-proposals/25.json, same for akash
        try:
            users[u['id']] = [u['username'], u['name']]
        except:
            users[u['id']] = [u['username'], u['trust_level']]

    # print("getCosmosUserMap", users)
    return users

epoch = datetime.datetime(1970, 1, 1)
def getEpochTime(createTime) -> int:
    current = datetime.datetime.strptime(createTime, "%Y-%m-%dT%H:%M:%S.%fZ")
    return int((current - epoch).total_seconds())

def unecode_text(msg):
    return urllib.parse.unquote(msg)


if __name__ == "__main__":
    # getCosmosUserMap("https://forum.cosmos.network/c/hub-proposals/25.json")
    pass