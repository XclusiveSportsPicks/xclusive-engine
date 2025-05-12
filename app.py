from flask import Flask, render_template, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Static sample picks (replace with real model output later)
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
    API_KEY = "1256c747dab65e1c3cd504f9a3f4802b"  # Provided Odds API Key

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
            continue  # Skip league if it fails

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

if __name__ == "__main__":
    app.run(debug=True)
