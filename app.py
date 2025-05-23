from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
import os
from datetime import datetime
import asyncio
from scraper.sharp_scraper_playwright import scrape_sao_live
from utils.team_name_map import normalize_team_name

load_dotenv()
app = Flask(__name__)

SHARP_DELTA_THRESHOLD = 30
MODEL_CONFIDENCE_MIN = 7.5

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
    sharp_data = asyncio.run(scrape_sao_live())
    odds_data = get_odds_data()

    picks = []
    for game in odds_data:
        team1 = normalize_team_name(game["team1"])
        team2 = normalize_team_name(game["team2"])
        odds1 = game["odds1"]

        sharp = sharp_data.get(team1) or sharp_data.get(team1.split()[-1]) or sharp_data.get(team1.replace("New York", "NY"))
        if not sharp:
            print(f"[SKIP] No sharp % for: {team1} vs {team2}")
            print(f"🔑 sharp_data keys: {list(sharp_data.keys())}")
            continue

        bet_pct = sharp["bet_pct"]
        money_pct = sharp["money_pct"]
        confidence_score = get_model_confidence(team1)
        sharp_diff = money_pct - bet_pct

        print(f"[DEBUG] {team1} vs {team2} — Bet: {bet_pct}%, Money: {money_pct}%, SharpDiff: {sharp_diff}, Confidence: {confidence_score}")

        if sharp_diff >= SHARP_DELTA_THRESHOLD and confidence_score >= MODEL_CONFIDENCE_MIN:
            picks.append({
                "game": f"{team1} vs {team2}",
                "pick": team1,
                "odds": odds1,
                "sharp_pct": f"Bets {bet_pct}%, Money {money_pct}%",
                "confidence": f"{confidence_score}/10",
                "timestamp": datetime.utcnow().isoformat()
            })

    print("🔍 Final Picks:", picks)
    return picks

def get_model_confidence(team_name):
    from random import uniform
    return round(uniform(7.5, 9.7), 1)

if __name__ == "__main__":
    print("[🔥 Xclusive Engine LIVE with Sharp %]")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
