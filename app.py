from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
import random

app = Flask(__name__)

# Static placeholder picks (for homepage rendering)
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

@app.route("/api/games")
def get_today_games_all_sports():
    API_KEY = "1256c747dab65e1c3cd504f9a3f4802b"

    leagues = [
        {"key": "baseball_mlb", "label": "MLB"},
        {"key": "basketball_nba", "label": "NBA"},
        {"key": "soccer_epl", "label": "Soccer EPL"},
        {"key": "americanfootball_nfl", "label": "NFL"},
        {"key": "icehockey_nhl", "label": "NHL"}
    ]

    all_games = []

    for league in leagues:
        url = f"https://api.the-odds-api.com/v4/sports/{league['key']}/odds/?apiKey={API_KEY}&regions=us&markets=h2h,spreads,totals&oddsFormat=american"
        response = requests.get(url)

        if response.status_code != 200:
            continue

        odds_data = response.json()

        for game in odds_data:
            teams = game.get("teams", [])
            time = game.get("commence_time", "")
            bookmakers = game.get("bookmakers", [])

            if bookmakers:
                book = bookmakers[0]
                markets = book.get("markets", [])
                odds_summary = {}

                for market in markets:
                    if market["key"] == "h2h":
                        for outcome in market["outcomes"]:
                            odds_summary[outcome["name"]] = outcome["price"]

                all_games.append({
                    "league": league["label"],
                    "teams": teams,
                    "time": time,
                    "odds": odds_summary,
                    "bookmaker": book.get("title", "N/A")
                })

    return jsonify({"games": all_games})

@app.route("/api/auto-picks")
def generate_auto_picks():
    API_KEY = "1256c747dab65e1c3cd504f9a3f4802b"

    leagues = [
        {"key": "baseball_mlb", "label": "MLB"},
        {"key": "basketball_nba", "label": "NBA"},
        {"key": "soccer_epl", "label": "Soccer EPL"}
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
    top_picks = sorted_picks[:5]

    if top_picks:
        top_picks[0]["confidence"] += " 🔥 X's Absolute Best Bet"

    return jsonify(top_picks)

if __name__ == "__main__":
    app.run(debug=True)
