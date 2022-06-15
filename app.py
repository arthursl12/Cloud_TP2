from flask import Flask
from flask import request

import datetime
import pickle
import urllib.request

urllib.request.urlretrieve("https://github.com/arthursl12/Cloud_TP2/raw/main/trained_model.sk", "trained_model.sk")
urllib.request.urlretrieve("https://github.com/arthursl12/Cloud_TP2/raw/main/last_updated.date", "last_updated.date")

app = Flask(__name__)
app.model = pickle.load(open("trained_model.sk", "rb"))
app.last_updated = pickle.load(open("last_updated.date", "rb"))

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/american", methods=["POST"])
def american_process():
    # Get input JSON
    text = request.get_json(force=False)['text']
    
    # Predict using the model
    result = app.model.predict([text])[0]
    print(result)
    
    # Convert datetime to ISO string
    date_string = datetime.datetime.strftime(
        app.last_updated, '%Y-%m-%dT%H:%M:%S%z'
    )
    
    # Send a dict response (Flask will convert to JSON
    return {
        "is_american": int(result),
        "version": "1.7",
        "model_date": date_string,
    }

