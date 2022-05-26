from discord import Webhook, RequestsWebhookAdapter
import discord

import datetime
import time

def sendConfirmation(webhookURL, signedUpForChains):
    embed = discord.Embed(
        title=f"SUCCESS!", 
        description=f"You have subscribed this channel to:\n{signedUpForChains}",
        # url="https://www.google.com",
        timestamp = datetime.datetime.utcnow(), # 
        color=0x00FF00
    ).set_thumbnail(url="https://cdn.pixabay.com/photo/2012/04/24/16/22/check-40319__480.png")
    webhook = Webhook.from_url(webhookURL, adapter=RequestsWebhookAdapter(sleep=False))
    webhook.send(username="Commonwealth Proposal",embed=embed) # Executing webhook
    time.sleep(0.2)