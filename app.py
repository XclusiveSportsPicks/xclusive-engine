from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# Cache picks for 10 minutes
CACHE = {
    "timestamp": None,
    "picks": []
}

# League definitions
LEAGUES = [
    {"key": "MLB", "emoji": "⚾️"},
    {"key": "NBA", "emoji": "🏀"},
    {"key": "NFL", "emoji": "🏈"},
    {"key": "NHL", "emoji": "🏒"},
    {"key": "SOCCER", "emoji": "⚽️"},
    {"key": "NCAAB", "emoji": "🎓"}
]

# Team pools per league
TEAM_BANK = {
    "MLB": ["Yankees", "Dodgers", "Astros", "Mets", "Cubs", "Guardians"],
    "NBA": ["Lakers", "Celtics", "Heat", "Knicks", "Warriors", "Nuggets"],
    "NFL": ["Eagles", "Chiefs", "Bills", "Cowboys", "49ers", "Packers"],
    "NHL": ["Rangers", "Bruins", "Maple Leafs", "Golden Knights", "Canucks", "Devils"],
    "SOCCER": ["Man City", "Liverpool", "Arsenal", "Chelsea", "Barcelona", "Real Madrid", "PSG", "Bayern", "Inter", "Atletico"],
    "NCAAB": ["Duke", "UNC", "Kansas", "Gonzaga", "Kentucky", "UCLA"]
}

# Simulate picks
def simulate_picks():
    picks = []
    for league in LEAGUES:
        for _ in range(1):  # One game per league
            teams = random.sample(TEAM_BANK[league["key"]], 2)
            chosen = random.choice(teams)
            odds = random.choice([-110, -120, +105, +115, +130])
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
                "league": league["key"],
                "emoji": league["emoji"],
                "game": f"{teams[0]} vs {teams[1]}",
                "pick": chosen,
                "odds": odds,
                "sharp": f"{sharp_pct}%",
                "confidence": confidence
            })

    # Sort and assign Best Bet 🔥
    picks = sorted(picks, key=lambda x: int(x["sharp"].strip('%')), reverse=True)
    if picks and "Elite" not in picks[0]["confidence"]:
        picks[0]["confidence"] += " 🔥 X's Absolute Best Bet"
    return picks

@app.route("/")
def index():
    return render_template("index.html", last_updated=datetime.now().strftime("%Y-%m-%d %H:%M"))

@app.route("/api/auto-picks")
def auto_picks():
    now = datetime.now()
    if CACHE["timestamp"] and now - CACHE["timestamp"] < timedelta(minutes=10):
        return jsonify(CACHE["picks"])
    picks = simulate_picks()
    CACHE["timestamp"] = now
    CACHE["picks"] = picks
    return jsonify(picks)

@app.route("/api/leagues")
def get_leagues():
    return jsonify([l["key"] for l in LEAGUES])

if __name__ == "__main__":
    app.run(debug=True)
