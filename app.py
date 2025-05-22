
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
import os
from datetime import datetime
from scraper.sharp_scraper import get_sharp_data
from utils.team_name_map import normalize_team_name

load_dotenv()
app = Flask(__name__)

SHARP_DELTA_THRESHOLD = 10
MODEL_CONFIDENCE_MIN = 6.0

@app.route("/")
def homepage():
    return render_template("index.html", picks=get_picks_data_only())

@app.route("/api/picks")
def get_picks():
    return jsonify({
        "generated_at": datetime.utcnow().isoformat(),
        "count": len(get_picks_data_only()),
        "picks": get_picks_data_only()
    })

def get_picks_data_only():
    from mlb.odds import get_odds_data
    sharp_data = get_sharp_data()
    odds_data = get_odds_data()

    picks = []

    for game in odds_data:
        team1 = normalize_team_name(game["team1"])
        team2 = normalize_team_name(game["team2"])
        odds1 = game["odds1"]

        sharp = sharp_data.get(team1)
        if not sharp:
            continue

        bet_pct = sharp["bet_pct"]
        money_pct = sharp["money_pct"]
        confidence_score = get_model_confidence(team1)
        sharp_diff = money_pct - bet_pct

        if sharp_diff >= SHARP_DELTA_THRESHOLD and confidence_score >= MODEL_CONFIDENCE_MIN:
            picks.append({
                "game": f"{team1} vs {team2}",
                "pick": team1,
                "odds": odds1,
                "sharp_pct": f"Bets {bet_pct}%, Money {money_pct}%",
                "confidence": f"{confidence_score}/10",
                "timestamp": datetime.utcnow().isoformat()
            })

    return picks

def get_model_confidence(team_name):
    # TEMP: mock scores that vary slightly for realism
    from random import uniform
    return round(uniform(7.5, 9.7), 1)

if __name__ == "__main__":
    print("[🔥 Xclusive Engine LIVE with Sharp %]")
    app.run(debug=True)
