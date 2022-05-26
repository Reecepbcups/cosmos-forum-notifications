# cosmos-forum-notifications

## IDEA
    website w/ mongo backend
    Webhook URL = login
    After pressing login, opens page of selections (juno, cosmos, osmo) etc. press save saves collection to mongo.
    Webhook, [chain1, chain2]

    My server checks for updates, if there is one, loop through all docs & send embed


# Setup
cp config_example.json ./website/config.json (May change location in future)
> edit values as needed


TODO easy way to use the same files within website & the normal code?
Just have normal code reach into websites?