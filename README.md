# cosmos-forum-notifications

## IDEA
    website w/ mongo backend
    Webhook URL = login
    After pressing login, opens page of selections (juno, cosmos, osmo) etc. press save saves collection to mongo.
    Webhook, [chain1, chain2]

    My server checks for updates, if there is one, loop through all collection docs & send embed


# Setup
```bash
cd src
cp example/config_example.json ../config.json # Edit values as needed

python3 -m pip install -r requirements/requirements.txt
```
## Running Notify script
```bash
cd src
python3 notify.py
```
## Running Website
```bash
cd src
python3 website/website.py
```

<br>

# Env Variables:
> Useful for Akash & public images. Put entire path in quotes
```js
Website:

MONGODB=mongodb://USER:PASS@localhost:27017/?authSource=admin
DATABASE=commonwealth_bot
COLLECTION=myCollection
PORT=8080

Notification Bot:

DEBUG_MODE=true
RUNNABLE_ENABLED=true
RUNNABLE_CHECK_EVERY=60
```

<br>

# Docker
## Website
```bash
cd src
sudo docker login

VERSION="1.0.2"
sudo docker build -t reecepbcups/commonwealth_notification_website:$VERSION -f website/Dockerfile .
sudo docker run -p 8080:8080 reecepbcups/commonwealth_notification_website:$VERSION
sudo docker push reecepbcups/commonwealth_notification_website:$VERSION
```

## Notification Bot
```bash
cd src
sudo docker login

VERSION="1.0.2"
sudo docker build -t reecepbcups/commonwealth_notification_bot:$VERSION -f Dockerfile .
sudo docker run -it reecepbcups/commonwealth_notification_bot:$VERSION
sudo docker push reecepbcups/commonwealth_notification_bot:$VERSION
```