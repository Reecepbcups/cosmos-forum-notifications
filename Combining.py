from pymongo import MongoClient
from discord import Webhook, RequestsWebhookAdapter
import discord
import datetime
import requests
import time
import urllib.parse

COMMON_WEALTH = {
    # 'Juno': 'https://commonwealth.im/api/bulkThreads?chain=juno&cutoff_date={ENCODED_UTC_TIME}&topic_id=853',
    'Osmosis': [
        'https://gov.osmosis.zone/api/bulkThreads?chain=osmosis&cutoff_date={ENCODED_UTC_TIME}&topic_id=679',
        'https://gov.osmosis.zone/discussion/{ID}',
        'https://info.osmosis.zone/static/media/logo.551f5780.png'
    ]
}
# EXAMPLE_DOCUMENTS = {
#     "https://discord.com/api/webhooks/978842076856848385/JPSTZf6loNnRw3jgR_JSlI_qd9EDR32QLEg6lXpN8Ca1yPbdqgF0WLsQnRj_3hXyEY3x": ['OSMO', "AKT", "COSMOS"],
#     "https://discord.com/api/webhooks/978842216627843072/vVz6zxYhtSF_gHTNcfhB9nAXzdgQTORvQRZ0wGtQ0R4oL3UB6vZUc_lrfkIS2qUtt33H": ['OSMO'],
# }

# same in Website.py
client = MongoClient('mongodb://root:akashmongodb19pass@782sk60c31ell6dbee3ntqc9lo.ingress.provider-2.prod.ewr1.akash.pub:31543/?authSource=admin')
db = client['reece']
coll = db['other']

def get_all_documents_in_collection():
    return coll.find({})

for doc in get_all_documents_in_collection():
    print(doc['url'], doc['enabledChains'])
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

def sendAnnouncement(chain, title, desc, url, image, **kwargs):
    # Have 2 embeds, one with desc shown. Allow user to change it in webapp?
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
            print(_theirWebhook[0:25], f" does not have notifs on for this chain! ({chain}->{enabled})")
            continue # they dont have notifs on for this

        webhook = Webhook.from_url(_theirWebhook, adapter=RequestsWebhookAdapter(sleep=False)) # Initializing webhook
        # error log if 503 error or something for rate limit?
        webhook.send(username="Commonwealth Proposal",embed=embed) # Executing webhook

def unecode_text(msg):
    return urllib.parse.unquote(msg)

for chainID, links in COMMON_WEALTH.items():
    api, discussions, img = links[0], links[1], links[2]

    threads = get_topic_list(api.format(ENCODED_UTC_TIME=getISO8601Time()), key="result")
    # print(threads.keys())
    
    sortedthreads = sorted(threads['threads'], key=lambda k: k['id'], reverse=True)

    for prop in sortedthreads:
        _id = prop['id']
        # print(i['id'], i['created_at'], i['title'])
        if prop['pinned'] == True: continue
        # if id < lastProp for this chain, continue

        title = unecode_text(prop['title'])
        createTime = prop['created_at']
        body = unecode_text(prop['body'])
        if len(body) > 2048:
            body = body[:2048] + "..."

        stage = str(prop['stage'])
        address = prop['Address']['address']

        print("breaking!"); break
        # print(_id, createTime, getEpochTime(createTime), title)

    sendAnnouncement(
        chainID,
        f"{chainID.title()} #{_id} CommonWealth {stage.title()}\n\n{title}", 
        f"", 
        url=discussions.format(ID=_id),
        image=img,
        Proposer_Address=address,
        # Stage=stage,
        Posted_Time=f"<t:{getEpochTime(createTime)}>",
        # MyWebsite="https://proposals.reece.sh",
        )
    # print(prop.keys())

    



