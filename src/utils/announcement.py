from discord import Webhook, RequestsWebhookAdapter
import discord

import datetime
import time

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
        embed.add_field(name=k.replace("_", " "), value=v, inline=False)

    for doc in collectionDocs:
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