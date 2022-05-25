
from flask import Flask, request, render_template, redirect, url_for, session, flash

from pymongo import MongoClient

# create new connection w/ mongo uri
client = MongoClient('mongodb://root:akashmongodb19pass@782sk60c31ell6dbee3ntqc9lo.ingress.provider-2.prod.ewr1.akash.pub:31543/?authSource=admin')
db = client['reece']
coll = db['other']

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

# TODO: Change to env variable in future
app.secret_key = 'BAD_SECRET_KEY'

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
    return render_template('main-page.html',  data=[{'chain': 'Juno'}, {'chain': 'Osmosis'}])

@app.route("/test" , methods=['GET', 'POST'])
def test():
    selectedChains = request.form.getlist('chains')
    # update_user(session['webhook'], selectedChains)
    print("NOT SAVING USER SINCE THIS IS A GOOD DB RN")
    return f"{session.get('webhook')} is now registered for: " + str(selectedChains)

# run the app
if __name__ == "__main__":
    app.run(debug=True, port=8080)