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
python3 -m pip install -r requirements/requirements.txt

## Docker
---

## Website
cd src
sudo docker login

VERSION="1.0.1"
sudo docker build -t reecepbcups/commonwealth_notification_website:$VERSION -f website/Dockerfile .
sudo docker run -p 8080:8080 reecepbcups/commonwealth_notification_website:$VERSION
sudo docker push reecepbcups/commonwealth_notification_website:$VERSION

## Notifcation Bot
cd src
sudo docker login

VERSION="1.0.1"
sudo docker build -t reecepbcups/commonwealth_notification_bot:$VERSION -f Dockerfile .
sudo docker run -it reecepbcups/commonwealth_notification_bot:$VERSION
sudo docker push reecepbcups/commonwealth_notification_bot:$VERSION

## Running Notify script
cd src
python3 notify.py