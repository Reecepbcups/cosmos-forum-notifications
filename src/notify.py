import os
import json
import time

from pymongo import MongoClient
from pymongo.collection import Collection

from utils.utils import getISO8601Time, getTopicList, getEpochTime, unecode_text
from utils.announcement import sendAnnouncement


last_props_file = "src/last_props.json"



def main(debugging: bool = False):
    # Load Database
    client = MongoClient(config['MongoDB'])
    db = client[config['Database']]
    coll = db[config['Collection']]

    '''Loads past saved proposals {chain: id}'''
    LATEST_PROP_IDS = getLastSavedProposalIDs()

    '''Runs notifications'''
    updatedPropIDs = run(LATEST_PROP_IDS, collection=coll, ignorePinned=True)

    '''Saves the update JSON chains and ids to file'''
    saveNewestProposalIDsToFile(updatedPropIDs)
    

def getLastSavedProposalIDs() -> dict:
    _lastIds = {} # {"osmosis": 555, "juno": 666, ...}
    if os.path.exists(last_props_file):
        f = open(last_props_file, 'r')
        _lastIds = json.load(f)
    return _lastIds
    
def saveNewestProposalIDsToFile(LATEST_PROPOSAL_IDS: dict):
    if len(LATEST_PROPOSAL_IDS.keys()) == 0: 
        print("LATEST_PROPOSAL_IDS is 0")
    with open(last_props_file, "w") as f:
        f.write(json.dumps(LATEST_PROPOSAL_IDS))
        print("SAVED FILE", LATEST_PROPOSAL_IDS)


def getAllDocuments(mongoCollection: Collection):
    return mongoCollection.find({})

# for doc in get_all_documents_in_collection():
#     print(doc['url'], doc['enabledChains'])
# exit()

def run(LAST_PROP_IDS: dict, collection: Collection, ignorePinned=True) -> dict:
    '''
    Running of notifications
    '''
    for chainID, (api, discussions, img) in COMMON_WEALTH.items():

        api = str(api).format(ENCODED_UTC_TIME=getISO8601Time())
        threads = getTopicList(api, key="result")['threads']

        print("\n" + chainID)

        for prop in sorted(threads, key=lambda k: k['id'], reverse=False):
            _id = prop['id']

            if ignorePinned and prop['pinned'] == True: continue

            if chainID not in LAST_PROP_IDS:
                print(f"{chainID} not in LAST_PROP_IDS. Set to {_id}")
                LAST_PROP_IDS[chainID] = _id

            # id the current propID is lower than what we have sent, skip it.
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

            sendAnnouncement( # chain, title, desc
                chain=chainID,
                title=f"{chainID.title()} #{_id} CommonWealth {stage.title()}\n\n{title}", 
                desc=body,  # This will be optional in the future
                url=discussions.format(ID=_id),
                image=img,
                collectionDocs=collection.find({}),
                debug=config["DEBUG"],
                Stage=stage,
                Proposer_Address=address,
                Posted_Time=f"<t:{getEpochTime(createTime)}>",
                # MyWebsite="https://proposals.reece.sh",
            )

    return LAST_PROP_IDS # Returns the chain ids so we can save


if __name__ == "__main__":
    
    with open("src/chains.json", 'r') as f:
        COMMON_WEALTH = dict(json.load(f)); # print(COMMON_WEALTH)
    with open("src/config.json") as f:
        config = json.load(f); # print(config)

    DEBUG_MODE = bool(os.getenv("DEBUG_MODE", config['DEBUG']))

    print(DEBUG_MODE)
    if DEBUG_MODE == False:
        print("Production Environment, waiting 2 seconds")
        time.sleep(2)

    # runnable
    main(debugging=DEBUG_MODE)