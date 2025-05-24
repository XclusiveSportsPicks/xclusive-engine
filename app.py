
from flask import Flask, render_template, jsonify
import subprocess
subprocess.run(["playwright", "install", "chromium"], check=True)

from dotenv import load_dotenv
import os
from datetime import datetime
import asyncio
import threading
from utils.team_name_map import normalize_team_name
from scraper.sharp_scraper_playwright import scrape_sao_live

load_dotenv()
app = Flask(__name__, template_folder="templates", static_folder="static")

SHARP_DELTA_THRESHOLD = 30
MODEL_CONFIDENCE_MIN = 7.5

sharp_data_cache = {}

def preload_sharp_data():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    sharp_data = loop.run_until_complete(scrape_sao_live())
    sharp_data_cache.update(sharp_data)

with app.app_context():
    threading.Thread(target=preload_sharp_data).start()

@app.route("/")
def homepage():
    try:
        picks = get_picks_data_only()
        return render_template("index.html", picks=picks)
    except Exception as e:
        import traceback
        return f"<h1>❌ Render Error</h1><pre>{traceback.format_exc()}</pre><hr><pre>{picks}</pre>", 500

@app.route("/api/picks")
def get_picks():
    picks = get_picks_data_only()
    return jsonify({
        "generated_at": datetime.utcnow().isoformat(),
        "count": len(picks),
        "picks": picks
    })

def get_picks_data_only():
    from mlb.odds import get_odds_data
    sharp_data = sharp_data_cache.copy()
    print('📈 Sharp cache:', sharp_data)
    odds_data = get_odds_data()
    print('📦 Raw odds data:', odds_data)

    picks = []

    for game in odds_data:
        team1 = normalize_team_name(game["team1"])
        team2 = normalize_team_name(game["team2"])
        odds1 = game["odds1"]

        sharp = sharp_data.get(team1) or sharp_data.get(team1.split()[-1]) or sharp_data.get(team1.replace("New York", "NY"))
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
                "sharp": f"{money_pct}%",
                "confidence": f"{confidence_score}/10"
            })

    print('✅ Final picks:', picks)
    return picks

def get_model_confidence(team_name):
    from random import uniform
    return round(uniform(7.5, 9.7), 1)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
