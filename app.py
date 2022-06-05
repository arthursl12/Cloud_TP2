from flask import Flask
from flask import request

import datetime
import pickle

app = Flask(__name__)
app.model = pickle.load(open("trained_model.sk", "rb"))
app.last_updated = pickle.load(open("last_updated.date", "rb"))

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/american", methods=["POST"])
def american_process():
    # Get input JSON
    text = request.get_json(force=False).text
    
    date_string = datetime.strptime(
        app.last_updated, '%Y-%m-%dT%H:%M:%S%z'
    ).isoformat()
    # Send a dict response (Flask will convert to JSON
    return {
        "is_american": 1,
        "version": "0.0",
        "model_date": date_string,
    }

