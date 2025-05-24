from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
from datetime import datetime
import asyncio
import threading
import os

from scraper.sharp_scraper_playwright import scrape_sao_live
from utils.team_name_map import normalize_team_name
from mlb.odds import get_odds_data

load_dotenv()
app = Flask(__name__, template_folder="templates", static_folder="static")

sharp_data_cache = {}

def preload_sharp_data():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    sharp_data = loop.run_until_complete(scrape_sao_live())
    sharp_data_cache.update(sharp_data)

# Start scraper in a background thread
with app.app_context():
    threading.Thread(target=preload_sharp_data).start()

@app.route("/")
def homepage():
    try:
        picks = get_picks_data_only()
        return render_template("index.html", picks=picks)
    except Exception as e:
        import traceback
        return f"<h1>❌ Render Error</h1><pre>{traceback.format_exc()}</pre>", 500

@app.route("/api/picks")
def get_picks():
    picks = get_picks_data_only()
    return jsonify({
        "generated_at": datetime.utcnow().isoformat(),
        "count": len(picks),
        "picks": picks
    })

def get_model_confidence(team_name):
    from random import uniform
    return round(uniform(7.5, 9.7), 1)

def get_picks_data_only():
    sharp_data = sharp_data_cache.copy()
    odds_data = get_odds_data()
    picks = []

    for game in odds_data:
        team1 = normalize_team_name(game["team1"])
        team2 = normalize_team_name(game["team2"])
        odds1 = game["odds1"]

        sharp = sharp_data.get(team1) or sharp_data.get(team1.split()[-1]) or sharp_data.get(team1.replace("New York", "NY"))
        if not sharp:
            print(f"[SKIP] No sharp % for: {team1} vs {team2}")
            continue

        bet_pct = sharp["bet_pct"]
        money_pct = sharp["money_pct"]
        sharp_diff = money_pct - bet_pct
        confidence_score = get_model_confidence(team1)

        print(f"[DEBUG] {team1} vs {team2} — Bet: {bet_pct}%, Money: {money_pct}%, SharpDiff: {sharp_diff}, Confidence: {confidence_score}")

        if confidence_score >= 9.0 and sharp_diff >= 15:
            confidence_tier = "High"
        elif confidence_score >= 8.0 and sharp_diff >= 20:
            confidence_tier = "Medium"
        elif confidence_score >= 7.5 and sharp_diff >= 25:
            confidence_tier = "Risk"
        else:
            continue

        picks.append({
            "game": f"{team1} vs {team2}",
            "pick": team1,
            "odds": odds1,
            "sharp_pct": f"Bets {bet_pct}%, Money {money_pct}%",
            "confidence": f"{confidence_score}/10",
            "confidence_tag": confidence_tier,
            "timestamp": datetime.utcnow().isoformat()
        })

    print("✅ Final Picks:", picks)
    return picks

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
