
from xml.dom.minidom import Document
from flask import Flask, request, render_template, redirect, url_for, session, flash

from utils.webutils import sendConfirmation

from pymongo import MongoClient
import json
import os

def update_user(url, enabledChains: list) -> bool:
    # update_user("testDisc", ["Juno", "Osmosis"])
    print("MongoDB Save:", url[0:25], enabledChains)
    q = coll.find_one({"url": url})
    if q is None:
        x = coll.insert_one({"url": url,"enabledChains": enabledChains}).inserted_id
    else:
        x = coll.update_one({"url": url}, {"$set": {"enabledChains": enabledChains}})
    return x is not None

app = Flask(__name__)

# https://testdriven.io/blog/flask-sessions/

app.secret_key = 'SOME_SECRET_SADKIONOJDASK'

@app.route('/')
def my_form():
    session['webhook'] = ""
    return render_template('login-form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    url = request.form['webhookURL']
    if not url.startswith("https://discord.com/api/webhooks/"):
        return redirect(url_for('my_form'))

    session['webhook'] = url
    return redirect(url_for('main_page'))

@app.route('/main')
def main_page():
    # myWebhook = session.get('webhook', None)
    # get users mongodb info here
    # chain names should be lowercase, match combining.py COMMON_WEALTH

    # get_all_chains_from_file
    with open(f"chains.json") as f:
        chains = json.load(f)
    temp = []
    for chainId in chains:
        temp.append({'chain': chainId})
    return render_template('main-page.html',  data=temp)

@app.route("/test" , methods=['GET', 'POST'])
def test():
    selectedChains = request.form.getlist('chains')
    update_user(session['webhook'], selectedChains)
    # ! TODO send webhook to channel?
    sendConfirmation(session['webhook'], selectedChains)
    return f"You are now registered for: " + str(selectedChains)

# @app.route("/reecetesting" , methods=['GET'])
# def DEBUG_getAllCollectionDocuments() -> Document:
#     return f"My documents: " + str(coll.find())

# run the app
if __name__ == "__main__":
    parent_dir = os.path.dirname(__file__)
    with open(f"config.json") as f:
        config = json.load(f)
        # print(config)
    
    mongoURI = str(os.environ.get('MONGODB', config['MongoDB']))
    database = str(os.environ.get('DATABASE', config['Database']))
    collection = str(os.environ.get('COLLECTION', config['Collection']))
    if mongoURI == "":
        print("MongoDB URI not found in environment variables or the config!")
    client = MongoClient(mongoURI)
    db = client[database]
    coll = db[collection]

    # confirm client works
    print("Client DB Names: " + str(client.list_database_names()))
    
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)