
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['webhookURL']
    processed_text = text.upper()
    print(processed_text)
    return processed_text

# run the app
if __name__ == "__main__":
    app.run(debug=True, port=8080)