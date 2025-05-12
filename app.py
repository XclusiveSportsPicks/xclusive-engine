from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
import random

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", last_updated=datetime.now().strftime("%Y-%m-%d %H:%M"))

@app.route("/api/auto-picks")
def generate_auto_picks():
    API_KEY = "1256c747dab65e1c3cd504f9a3f4802b"

    leagues = [
        {"key": "baseball_mlb", "label": "MLB"},
        {"key": "basketball_nba", "label": "NBA"},
        {"key": "americanfootball_nfl", "label": "NFL"},
        {"key": "icehockey_nhl", "label": "NHL"},
        {"key": "soccer_epl", "label": "Soccer EPL"},
        {"key": "soccer_usa_mls", "label": "Soccer MLS"},
        {"key": "soccer_spain_la_liga", "label": "Soccer La Liga"},
        {"key": "soccer_italy_serie_a", "label": "Soccer Serie A"},
        {"key": "soccer_germany_bundesliga", "label": "Soccer Bundesliga"},
        {"key": "soccer_france_ligue_one", "label": "Soccer Ligue 1"},
        {"key": "soccer_uefa_champs_league", "label": "Soccer UCL"},
        {"key": "soccer_south_america_copa_libertadores", "label": "Copa Libertadores"},
        {"key": "soccer_international_friendly", "label": "Intl Soccer"}
    ]

    picks = []

    for league in leagues:
        url = f"https://api.the-odds-api.com/v4/sports/{league['key']}/odds/?apiKey={API_KEY}&regions=us&markets=h2h&oddsFormat=american"
        response = requests.get(url)
        if response.status_code != 200:
            continue

        data = response.json()
        for game in data:
            if not game.get("bookmakers"):
                continue

            team_a, team_b = game["teams"]
            outcomes = game["bookmakers"][0]["markets"][0]["outcomes"]

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

    sorted_picks = sorted(picks, key=lambda x: int(x["sharp"].strip('%')), reverse=True)
    top_picks = sorted_picks[:7]

    if top_picks:
        top_picks[0]["confidence"] += " 🔥 X's Absolute Best Bet"

    return jsonify(top_picks)

@app.route("/api/leagues")
def get_league_list():
    return jsonify([
        "MLB", "NBA", "NFL", "NHL",
        "Soccer EPL", "Soccer MLS", "Soccer La Liga", "Soccer Serie A",
        "Soccer Bundesliga", "Soccer Ligue 1", "Soccer UCL",
        "Copa Libertadores", "Intl Soccer"
    ])

if __name__ == "__main__":
    app.run(debug=True)
