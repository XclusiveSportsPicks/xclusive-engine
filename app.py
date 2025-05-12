from flask import Flask, render_template, jsonify
import requests
from datetime import datetime, timedelta
import random
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Simple in-memory cache
CACHE = {
    "timestamp": None,
    "picks": []
}

@app.route("/")
def index():
    return render_template("index.html", last_updated=datetime.now().strftime("%Y-%m-%d %H:%M"))

@app.route("/api/auto-picks")
def generate_auto_picks():
    now = datetime.now()
    if CACHE["timestamp"] and now - CACHE["timestamp"] < timedelta(minutes=10):
        logging.info("Using cached picks.")
        return jsonify(CACHE["picks"])

    API_KEY = "1256c747dab65e1c3cd504f9a3f4802b"

    leagues = [
        {"key": "baseball_mlb", "label": "MLB"},
        {"key": "basketball_nba", "label": "NBA"},
        {"key": "soccer_epl", "label": "Soccer EPL"},
        {"key": "americanfootball_nfl", "label": "NFL"},
        {"key": "icehockey_nhl", "label": "NHL"},
        {"key": "basketball_ncaab", "label": "NCAAB"}
    ]

    picks = []

    for league in leagues:
        url = f"https://api.the-odds-api.com/v4/sports/{league['key']}/odds/?apiKey={API_KEY}&regions=us&markets=h2h&oddsFormat=american"
        logging.info(f"Requesting: {league['label']} - {url}")
        response = requests.get(url)
        if response.status_code != 200:
            logging.warning(f"Failed to load {league['label']}: Status {response.status_code}")
            continue

        data = response.json()
        logging.info(f"{league['label']} - Games found: {len(data)}")

        for game in data:
            if not game.get("bookmakers"):
                continue

            markets = game["bookmakers"][0].get("markets", [])
            if not markets or not markets[0].get("outcomes"):
                continue

            outcomes = markets[0]["outcomes"]
            teams = game.get("teams", ["Unknown A", "Unknown B"])
            if len(teams) < 2:
                teams = ["Unknown A", "Unknown B"]

            team_a, team_b = teams
            chosen = random.choice(outcomes)
            sharp_pct = random.randint(60, 94)

            if sharp_pct >= 88:
                confidence = "Elite 🔒 Max Confidence"
            elif sharp_pct > 72:
                confidence = "High"
            elif sharp_pct > 66:
                confidence = "Medium"
            else:
                confidence = "Low"

            picks.append({
                "league": league["label"],
                "game": f"{team_a} vs. {team_b}",
                "pick": chosen["name"],
                "odds": chosen["price"],
                "sharp": f"{sharp_pct}%",
                "confidence": confidence,
                "status": "Projected",
                "result": ""
            })

    picks = sorted(picks, key=lambda x: int(x["sharp"].strip('%')), reverse=True)
    top_picks = picks[:7]

    if top_picks and "Elite" not in top_picks[0]["confidence"]:
        top_picks[0]["confidence"] += " 🔥 X's Absolute Best Bet"

    CACHE["timestamp"] = now
    CACHE["picks"] = top_picks

    logging.info(f"Total picks generated: {len(top_picks)}")
    return jsonify(top_picks)

@app.route("/api/leagues")
def get_league_list():
    return jsonify(["MLB", "NBA", "Soccer EPL", "NFL", "NHL", "NCAAB"])

if __name__ == "__main__":
    app.run(debug=True)
