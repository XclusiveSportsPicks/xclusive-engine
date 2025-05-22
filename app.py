# app.py
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
import requests
import os
from datetime import datetime

# Load .env values
load_dotenv()

app = Flask(__name__)

# === Config ===
ODDS_API_KEY = os.getenv("ODDS_API_KEY")
ODDS_API_URL = "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"
SHARP_DELTA_THRESHOLD = 30
MODEL_CONFIDENCE_MIN = 7.5

# === Homepage Route (HTML Dashboard) ===
@app.route("/")
def homepage():
    picks = get_picks_data_only()
    return render_template("index.html", picks=picks)

# === API Route ===
@app.route("/api/picks")
def get_picks():
    try:
        picks = get_picks_data_only()
        return jsonify({
            "generated_at": datetime.utcnow().isoformat(),
            "count": len(picks),
            "picks": picks
        })
    except Exception as e:
        return jsonify({"error": "Live odds fetch failed", "details": str(e)}), 503

# === Core Logic Shared by API and Frontend ===
def get_picks_data_only():
    response = requests.get(ODDS_API_URL, params={
        "regions": "us",
        "markets": "h2h",
        "oddsFormat": "american",
        "apiKey": ODDS_API_KEY
    })
    response.raise_for_status()
    data = response.json()

    picks = []
    for game in data:
        if not game.get("bookmakers"):
            continue

        bookmaker = game["bookmakers"][0]
        markets = bookmaker.get("markets", [])
        if not markets:
            continue

        outcomes = markets[0].get("outcomes", [])
        if len(outcomes) < 2:
            continue

        team_1 = outcomes[0]["name"]
        team_2 = outcomes[1]["name"]
        odds_1 = outcomes[0]["price"]

        bet_pct = get_bet_percentage(team_1)
        money_pct = get_money_percentage(team_1)
        model_score = get_model_confidence(team_1)

        sharp_diff = money_pct - bet_pct

        if sharp_diff >= SHARP_DELTA_THRESHOLD and model_score >= MODEL_CONFIDENCE_MIN:
            picks.append({
                "game": f"{team_1} vs {team_2}",
                "pick": team_1,
                "odds": odds_1,
                "sharp_pct": f"Bets {bet_pct}%, Money {money_pct}%",
                "confidence": f"{model_score}/10",
                "timestamp": datetime.utcnow().isoformat()
            })

    return picks

# === Replace these with real sportsbook/model logic soon ===
def get_bet_percentage(team_name): return 44
def get_money_percentage(team_name): return 78
def get_model_confidence(team_name): return 8.6

# === Run Flask App Locally ===
if __name__ == "__main__":
    print("[🚀 Xclusive Engine Booting]")
    app.run(debug=True)
