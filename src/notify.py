import os
import json
import time
import schedule

from pymongo import MongoClient
from pymongo.collection import Collection

from utils.utils import getISO8601Time, getTopicList, getCosmosUserMap, getEpochTime, unecode_text
from utils.announcement import sendAnnouncement


last_props_file = "last_props.json"


def main(debugging: bool = False):
    # Load Database - Make same as Website.py
    mongoURI = str(os.environ.get('MONGODB', config['MongoDB']))
    database = str(os.environ.get('DATABASE', config['Database']))
    collection = str(os.environ.get('COLLECTION', config['Collection']))    
    client = MongoClient(mongoURI)
    db = client[database]
    coll = db[collection]    

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

        # https://forum.cosmos.network/c/hub-proposals/25.json
        # ['topic_list']['topics']
        # ignore ['pinned']
        # if chainId == "cosmos", we do other things

    for chainID, (api, discussions, img) in COMMON_WEALTH.items():

        if chainID != "akash":
            continue # DEBUGGING

        userIDToName = {}
        api = str(api)
        if chainID == "cosmos" or chainID == "akash":
            # ['id', 'title', 'fancy_title', 'slug', 'posts_count', 'reply_count', 'highest_post_number', 'image_url', 
            # 'created_at', 'last_posted_at', 'bumped', 'bumped_at', 'archetype', 'unseen', 'pinned', 'unpinned', \
            # 'excerpt', 'visible', 'closed', 'archived', 'bookmarked', 'liked', 'tags', 'tags_descriptions', 'views', 
            # 'like_count', 'has_summary', 'last_poster_username', 'category_id', 'pinned_globally', 'featured_link', 
            # 'has_accepted_answer', 'posters'])
            userIDToName = getCosmosUserMap(api)
            threads = getTopicList(api, key="topic_list")['topics']
            
        else:
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

            body = ""
            stage = ""
            address = ""
            originalPoster = ""
            
            # Should probably turn this into a dict 'switch' statement
            # which returns the JSON values. Then just pass through the the sendAnnouncement as kwargs
            if 'body' in prop: # cosmos forum doesn't have body, so this if for all other chains
                body = unecode_text(prop['body']) 
                if len(body) > 2048:
                    body = body[:2048] + "..."
                    stage = str(prop['stage'])
                    address = prop['Address']['address']
            else:
                # Standalone forums
                if chainID == "cosmos":
                    for poster in prop['posters']:
                        desc = str(poster['description'])
                        if 'original' in desc.lower():
                            userID = poster['user_id'] 
                            username = userIDToName[userID][0]
                            name = userIDToName[userID][1]
                            originalPoster = f"{name} ( https://forum.cosmos.network/u/{username} )"

                elif chainID == "akash": # merge these together with cosmos in the future
                    for poster in prop['posters']:
                        desc = str(poster['description'])
                        if 'original' in desc.lower():
                            userID = poster['user_id']
                            username = userIDToName[userID][0]
                            # trustLevel = userIDToName[userID][1] # future?
                            originalPoster = f"{username} https://forum.akash.network/u/{username}"

            # Update this prop to newest
            LAST_PROP_IDS[chainID] = _id
            print(_id, createTime, getEpochTime(createTime), title)
            # print("breaking!"); break

            # Sends kwargs which are not blank
            sendAnnouncement( # chain, title, desc
                chain=chainID,
                title=f"{chainID.title()} #{_id} CommonWealth {stage.title()}\n\n{title}", 
                desc=body,  # This will be optional in the future
                url=discussions.format(ID=_id),
                image=img,
                collectionDocs=collection.find({}),
                debug=config["DEBUG"],
                Stage=stage,
                Proposer=originalPoster,
                Proposer_Address=address,
                Posted_Time=f"<t:{getEpochTime(createTime)}>",
                # MyWebsite="https://proposals.reece.sh",
            )

    return LAST_PROP_IDS # Returns the chain ids so we can save




if __name__ == "__main__":
    
    with open("chains.json", 'r') as f:
        COMMON_WEALTH = dict(json.load(f)); # print(COMMON_WEALTH)
    
    # try catch
    try:
        with open("config.json") as f:
            config = json.load(f); # print(config)        
    except:
        config = {}
        print(os.path.abspath(__file__))
        print("You did not 'cp src/example/config_example.json src/config.json'")

    DEBUG_MODE = bool(os.getenv("DEBUG_MODE", config['DEBUG']))

    RUNNABLE = bool(os.getenv("RUNNABLE_ENABLED", config['RUNNABLE']['ENABLED']))
    RUNNABLE_MINUTES = int(os.getenv("RUNNABLE_CHECK_EVERY", config['RUNNABLE']['CHECK_EVERY']))

    

    print(f"DEBUG_MODE={DEBUG_MODE}")
    if DEBUG_MODE == False:
        print("Production Environment, waiting 2 seconds")
        time.sleep(2)

    if RUNNABLE:
        # use schedular
        print(f"RUNNABLE ENABLED, running every: {RUNNABLE_MINUTES} minutes")
        main() # Call 1 time first
        schedule.every(RUNNABLE_MINUTES).minutes.do(main)
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        print("Single run...")
        main(debugging=DEBUG_MODE)