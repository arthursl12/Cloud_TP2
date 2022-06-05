from flask import Flask
from flask import request

app = Flask(__name__)
app.model = pickle.load(open("*.sk", "rb"))

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/american", methods=["POST"])
def american_process():
    # Get input JSON
    text = request.get_json(force=False).text
    
    
    
    # Send a dict response (Flask will convert to JSON
    return {
        "is_american": 1,
        "version": "0.0",
        "model_date": 
    }

