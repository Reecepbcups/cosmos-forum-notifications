# https://forum.cosmos.network/c/hub-proposals/25.json

# topic_list
# https://github.com/hicommonwealth/commonwealth


COMMON_WEALTH = {
    'juno': 'https://commonwealth.im/api/bulkThreads?chain=juno&cutoff_date={ENCODED_UTC_TIME}&topic_id=853',
    'osmosis': 'https://gov.osmosis.zone/api/bulkThreads?chain=osmosis&cutoff_date={ENCODED_UTC_TIME}&topic_id=679'
}

'''
Future: Common Wealth
- https://gov.osmosis.zone/discussion/5032-evmos-incentivized-pool-matched-incentives

- https://gov.osmosis.zone/api/bulkThreads?chain=osmosis&topic_id=679
-  https://gov.osmosis.zone/api/bulkOffchain?chain=osmosis&community=&jwt= # Shows id of 679
- https://gov.osmosis.zone/api/status
'''

import requests
import time

# We dump this to file every run since we update the lastID
forums = {
    'cosmos': { # This could be opened up to allow other forum categories as well? like https://forum.cosmos.network/c/conversation/34.json
        'api': 'https://forum.cosmos.network/c/hub-proposals/25.json', # https://forum.cosmos.network/c/hub-proposals/25
        'lastID': 6614
    }
}

def main():
    # dict_keys(['can_create_topic', 'more_topics_url', 'per_page', 'top_tags', 'topics'])

    forum = forums['cosmos'] # so we can support many

    data = get_topic_list(forum['api'])

    data = sorted(data['topics'], key=lambda k: k['created_at'], reverse=True)
    
    for prop in data:
        # print(i['id'], i['created_at'], i['title'])
        if prop['pinned'] == True: continue
        
    exit()

def get_topic_list(url, key="topic_list") -> dict:
    response = requests.get(url)
    data = response.json()
    if key in data:
        data = data[key]
    return data

def compare_iso_times(time1, time2):
    '''
    when given 2 iso times, return the higher value
    
    example:
    2022-05-23T18:41:09.734Z and 2022-04-07T16:58:01.590Z
    = time1 is newer, so we should past this. Then save it to cache
    '''
    time1 = time.strptime(time1, "%Y-%m-%dT%H:%M:%S.%fZ")
    time2 = time.strptime(time2, "%Y-%m-%dT%H:%M:%S.%fZ")
    # print(time1, time2)
    if time1 > time2:
        return True
    return False

# lastProposalID = 6614
# sorted = {}

# for prop in data['topics']:
#     if prop['pinned'] == True:
#         continue
#     _id = prop['id']
#     title = prop['title']
#     views = prop['views']
#     created_at = prop['created_at']

#     sorted[created_at] = {
#         "title": title,
#         "views": views,
#         "_id": _id
#     }
#     print(f"id={_id} | {title} {views} views  {created_at}")


# print(sorted.keys())
# lastPost = "2022-05-21T07:42:21.285Z"
# for createTime, obj in sorted.items():
#     if compare_iso_times(createTime, lastPost):
#         lastPost = createTime
#         lastProposalID = obj['_id']
#         print(f"{lastProposalID} {obj['title']} {obj['views']} views {createTime}")


if __name__ == "__main__":
    main()