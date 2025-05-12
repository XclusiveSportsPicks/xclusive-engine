from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
import random
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/")
def index():
    return render_template("index.html", last_updated=datetime.now().strftime("%Y-%m-%d %H:%M"))

@app.route("/api/auto-picks")
def generate_auto_picks():
    API_KEY = "1256c747dab65e1c3cd504f9a3f4802b"

    leagues = [
        {"key": "baseball_mlb", "label": "MLB"},
        {"key": "basketball_nba", "label": "NBA"}
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
                logging.info("Skipped: No bookmakers")
                continue

            markets = game["bookmakers"][0].get("markets", [])
            if not markets or not markets[0].get("outcomes"):
                logging.info("Skipped: No valid markets")
                continue

            if not game.get("teams") or len(game["teams"]) < 2:
                logging.info("Skipped: Missing teams")
                continue

            outcomes = markets[0]["outcomes"]
            team_a, team_b = game["teams"]
            chosen = random.choice(outcomes)
            sharp_pct = random.randint(60, 78)
            confidence = "High" if sharp_pct > 72 else "Medium" if sharp_pct > 66 else "Low"

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

    logging.info(f"Total picks generated: {len(picks)}")

    sorted_picks = sorted(picks, key=lambda x: int(x["sharp"].strip('%')), reverse=True)
    top_picks = sorted_picks[:7]

    if top_picks:
        top_picks[0]["confidence"] += " 🔥 X's Absolute Best Bet"

    return jsonify(top_picks)

@app.route("/api/leagues")
def get_league_list():
    return jsonify(["MLB", "NBA"])

if __name__ == "__main__":
    app.run(debug=True)
