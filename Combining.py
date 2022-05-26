import json
from pymongo import MongoClient
from discord import Webhook, RequestsWebhookAdapter
import discord
import datetime
import requests
import time
import urllib.parse
import os

last_props_file = "last_props.json"

with open("chains.json", 'r') as f:
    COMMON_WEALTH = dict(json.load(f))
    # print(COMMON_WEALTH)

with open("config.json") as f:
    config = json.load(f)
    # print(config)

if config['DEBUG'] == False:
    print("Production Environment, waiting 2 seconds")
    time.sleep(2)
else:
    print("In debug mode!")
    time.sleep(5)

# Load Database
client = MongoClient(config['MongoDB'])
db = client[config['Database']]
coll = db[config['Collection']]

def get_all_documents_in_collection():
    return coll.find({})

# for doc in get_all_documents_in_collection():
#     print(doc['url'], doc['enabledChains'])
# exit()

def getISO8601Time(encode=True):
    output = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z"
    if encode: output = output.replace(":", "%3A")
    return output

def get_topic_list(url, key="topic_list") -> dict:
    response = requests.get(url)
    data = response.json()
    if key in data:
        data = data[key]
    return data

epoch = datetime.datetime(1970, 1, 1)
def getEpochTime(createTime) -> int:
    current = datetime.datetime.strptime(createTime, "%Y-%m-%dT%H:%M:%S.%fZ")
    return int((current - epoch).total_seconds())

def sendAnnouncement(chain, title, desc, url, image, debug=False, **kwargs):
    # Have 2 embeds, one with desc shown. Allow user to change it in webapp?
    # if debug, it does NOT send the webhooks. Just prints embed values
    embed = discord.Embed(
        title=f"{title}", 
        description=desc, # 
        url=url,
        timestamp = datetime.datetime.utcnow(), # 
        color=0xFFFFFF
    ).set_thumbnail(url=image)

    for k, v in kwargs.items():
        embed.add_field(name=k.replace("_", " "), value=v, inline=False)

    for doc in get_all_documents_in_collection():
        _theirWebhook = doc['url']
        enabled = doc['enabledChains']
        if chain not in enabled:
            # print(_theirWebhook[0:40] + "...", f" does not have notifs on for this chain! ({chain} not in: {enabled})")
            continue

        if debug == False:
            webhook = Webhook.from_url(_theirWebhook, adapter=RequestsWebhookAdapter(sleep=False)) # Initializing webhook
            # error log if 503 error or something for rate limit?
            webhook.send(username="Commonwealth Proposal",embed=embed) # Executing webhook
            time.sleep(1.21) # 50 per minutes = 1.2sec per post
        else:
            # print(f"debug={debug} so not posting to discord\n")
            break

def unecode_text(msg):
    return urllib.parse.unquote(msg)


LAST_PROP_IDS = {}
if os.path.exists(last_props_file):
    f = open(last_props_file, 'r')
    LAST_PROP_IDS = json.load(f)
    # print(f"Loaded last props id from file: {LAST_PROP_IDS}")

# for debugging
# LAST_PROP_IDS = {"osmosis": 5030, "juno": 4883}

for chainID, links in COMMON_WEALTH.items():
    api, discussions, img = links[0], links[1], links[2]

    threads = get_topic_list(api.format(ENCODED_UTC_TIME=getISO8601Time()), key="result")
    # print(threads.keys())

    sortedThreads = sorted(threads['threads'], key=lambda k: k['id'], reverse=False)

    print("\n" + chainID)
    for prop in sortedThreads:
        _id = prop['id']

        if chainID not in LAST_PROP_IDS:
            print(f"{chainID} not in LAST_PROP_IDS. Set to {_id}")
            LAST_PROP_IDS[chainID] = _id
        # print(f"ID: {_id} -> my current prop ID: {LAST_PROP_IDS[chainID]}")

        # print(i['id'], i['created_at'], i['title'])
        # if prop['pinned'] == True: continue


        if _id <= LAST_PROP_IDS[chainID]:
            # print(_id, chainID, "Already did this")
            continue

        title = unecode_text(prop['title'])
        createTime = prop['created_at']
        body = unecode_text(prop['body'])
        if len(body) > 2048:
            body = body[:2048] + "..."

        stage = str(prop['stage'])
        address = prop['Address']['address']

        # Update this prop to newest
        LAST_PROP_IDS[chainID] = _id
        print(_id, createTime, getEpochTime(createTime), title)
        # print("breaking!"); break

        sendAnnouncement(
            chainID,
            f"{chainID.title()} #{_id} CommonWealth {stage.title()}\n\n{title}", 
            f"", 
            url=discussions.format(ID=_id),
            image=img,
            debug=config["DEBUG"],
            Proposer_Address=address,
            # Stage=stage,
            Posted_Time=f"<t:{getEpochTime(createTime)}>",
            # MyWebsite="https://proposals.reece.sh",
        )

# saves cache of all chains after they all run
with open("last_props.json", "w") as f:
    f.write(json.dumps(LAST_PROP_IDS))
    print("SAVED FILE", LAST_PROP_IDS)