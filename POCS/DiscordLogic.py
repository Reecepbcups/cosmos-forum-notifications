import pymongo
from discord import Webhook, RequestsWebhookAdapter
import discord
import datetime

EXAMPLE_DOCUMENTS = {
    "https://discord.com/api/webhooks/978842076856848385/JPSTZf6loNnRw3jgR_JSlI_qd9EDR32QLEg6lXpN8Ca1yPbdqgF0WLsQnRj_3hXyEY3x": ['OSMO', "AKT", "COSMOS"],
    "https://discord.com/api/webhooks/978842216627843072/vVz6zxYhtSF_gHTNcfhB9nAXzdgQTORvQRZ0wGtQ0R4oL3UB6vZUc_lrfkIS2qUtt33H": ['OSMO'],
}

def main():
    # sendAnnouncement("test title", "some desc")
    print(getISO8601Time())
    pass

def sendAnnouncement(title, desc):
    embed = discord.Embed(
        title=f"{title}", 
        description=desc, # <t:epochtime>
        timestamp=datetime.datetime.utcnow(), 
        color=0xFFFFFF
    )
    embed.add_field(name="Note", value=f"https://reece.sh", inline=False)
    embed.set_thumbnail(url="https://media.moddb.com/images/members/5/4550/4549205/duck.jpg")

    for WEBHOOK_URL in EXAMPLE_DOCUMENTS.keys():
        webhook = Webhook.from_url(WEBHOOK_URL, adapter=RequestsWebhookAdapter(sleep=False)) # Initializing webhook
        # log errors for them to see?
        webhook.send(username="Commonwealth Proposal",embed=embed) # Executing webhook




def loopThroughOsmosisPropsEx():
    for i in range(275, 284):
        yield i

def checkProposals():
    current = { # load from file
        "OSMO": 282,
        "AKT": 40,
        "COSMOS": 71
    }

    for orderedPropID in loopThroughOsmosisPropsEx():
        if orderedPropID > current["OSMO"]:
            # title, desc, when it was posted, etc
            sendAnnouncement(f"OSMO Proposal on commonwealth #{orderedPropID}", "https://osmosis.proposals.reece.sh/proposal/" + str(orderedPropID))
            current["OSMO"] = orderedPropID
        else:
            print(f"{orderedPropID} is not greater than {current['OSMO']}")


    # dump ids to file

# checkProposals()

def getISO8601Time(encode=True):
    output = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z"
    if encode: output = output.replace(":", "%3A")
    return output



if __name__ == "__main__":
    main()