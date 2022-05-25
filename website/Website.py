
from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)

# https://testdriven.io/blog/flask-sessions/
app.secret_key = 'BAD_SECRET_KEY'

@app.route('/')
def my_form():
    return render_template('login-form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['webhookURL']
    # processed_text = text.upper()
    # print(processed_text)
    # session['webhook'] = text
    # return processed_text
    return redirect(url_for('main_page'))
    
@app.route("/test" , methods=['GET', 'POST'])
def test():
    select = request.form.getlist('chains')
    return(str(select)) # just to see what select is

@app.route('/main')
def main_page():
    # myWebhook = session.get('webhook', None)
    return render_template('main-page.html',  data=[{'chain': 'Juno'}, {'chain': 'Osmosis'}])

# run the app
if __name__ == "__main__":
    app.run(debug=True, port=8080)