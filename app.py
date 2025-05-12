from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Simulated picks database (can be replaced with real DB later)
picks = [
    {
        "game": "Yankees vs. Red Sox",
        "pick": "Yankees ML",
        "odds": "-120",
        "confidence": "High",
        "sharp": "68%",
        "status": "Confirmed",
        "result": "Win"
    },
    {
        "game": "Lakers vs. Warriors",
        "pick": "Warriors +4.5",
        "odds": "-110",
        "confidence": "Medium",
        "sharp": "72%",
        "status": "In Progress",
        "result": ""
    }
]

@app.route("/")
def index():
    return render_template("index.html", picks=picks, last_updated=datetime.now().strftime("%Y-%m-%d %H:%M"))

@app.route("/api/picks", methods=["GET"])
def get_picks():
    return jsonify(picks)

@app.route("/api/picks", methods=["POST"])
def add_pick():
    data = request.get_json()
    picks.append(data)
    return jsonify({"message": "Pick added successfully"}), 201

if __name__ == "__main__":
    app.run(debug=True)
