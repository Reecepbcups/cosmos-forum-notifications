# cosmos-forum-notifications

## IDEA
    website w/ mongo backend
    Webhook URL = login
    After pressing login, opens page of selections (juno, cosmos, osmo) etc. press save saves collection to mongo.
    Webhook, [chain1, chain2]

    My server checks for updates, if there is one, loop through all docs & send embed


# Setup
cd src
cp example/config_example.json ../config.json
> edit values as needed

## Docker
cd src
sudo docker build -t reecepbcups/commonwealth_notification_website -f website/Dockerfile .
sudo docker run -p 8080:8080 reecepbcups/commonwealth_notification_website

sudo docker login
sudo docker push reecepbcups/commonwealth_notification_website

## Running Notify script
python3 src/notify.py