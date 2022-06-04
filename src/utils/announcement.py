from discord import Webhook, RequestsWebhookAdapter
import discord

import datetime
import time
import json
import os

from pymongo import MongoClient

def sendAnnouncement(chain, title, desc, url, image, collectionDocs, debug=False, **kwargs):
    # Have 2 embeds, one with desc shown. Allow user to change it in webapp?
    # if debug, it does NOT send the webhooks. Just prints embed values
    embed = discord.Embed(
        title=f"{title}", 
        # description=desc,
        description="",
        url=url,
        timestamp = datetime.datetime.utcnow(), # 
        color=0xFFFFFF
    ).set_thumbnail(url=image)

    for k, v in kwargs.items():
        if len(v) > 0:
            embed.add_field(name=k.replace("_", " "), value=v, inline=False)

    # for idx, doc in enumerate(collectionDocs):
    #     print(idx, doc)

    for doc in collectionDocs:
        _theirWebhook = doc['url']
        enabled = doc['enabledChains']
        if chain not in enabled and chain != "debugtest":
            # print(_theirWebhook[0:40] + "...", f" does not have notifs on for this chain! ({chain} not in: {enabled})")
            print("skipping...")
            continue

        if debug == False:
            webhook = Webhook.from_url(_theirWebhook, adapter=RequestsWebhookAdapter(sleep=False))
            # Check return here, if there is no webhook, remove from DB
            webhook.send(username="Commonwealth Proposal",embed=embed)
            time.sleep(1.21) # 50 per minutes = 1.2sec per post
        else:
            # print(f"debug={debug} so not posting to discord\n")
            break

def DEBUG_RUN_FOR_ALL():
    print("DEBUG_RUN_FOR_ALL'")
    sendAnnouncement( # chain, title, desc
        chain="debugtest",
        title=f"{'test'} #{'t'} CommonWealth {'ex'.title()}\n\n{'here is the title'}", 
        desc="my body",  # This will be optional in the future
        url="https://myURL.com".format(ID=5),
        image="",
        collectionDocs=coll.find(),
        debug=False,
        # Stage=stage,
        # Proposer_Address=address,
        # Posted_Time=f"<t:{getEpochTime()}>",
        # MyWebsite="https://proposals.reece.sh",
    )

    # for doc in coll.find():
    #     print(doc)

if __name__ == '__main__':

    # try catch
    try:
        with open("config.json") as f:
            config = json.load(f); # print(config)        
    except:
        config = {}
        print(os.path.abspath(__file__))
        print("You did not 'cp src/example/config_example.json src/config.json'")

    uri = config['MongoDB']
    dbName = config['Database']
    collName = config['Collection']
    client = MongoClient(uri)
    db = client[dbName]
    coll = db[collName]  

    print(uri, dbName, collName)

    DEBUG_RUN_FOR_ALL()