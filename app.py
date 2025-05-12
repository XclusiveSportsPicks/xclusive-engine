from flask import Flask, render_template, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Static example picks (these can be replaced by live-generated ones later)
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

# Homepage route
@app.route("/")
def index():
    return render_template("index.html", picks=picks, last_updated=datetime.now().strftime("%Y-%m-%d %H:%M"))

# API route for getting current picks
@app.route("/api/picks", methods=["GET"])
def get_picks():
    return jsonify(picks)

# NEW API route to pull today's MLB schedule & odds from The Odds API
@app.route("/api/games")
def get_today_mlb_games():
    API_KEY = "1256c747dab65e1c3cd504f9a3f4802b "  # Replace with your key or load from environment
    url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds/?apiKey={API_KEY}&regions=us&markets=h2h,spreads,totals&oddsFormat=american"
    
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data", "status": response.status_code}), 500

    odds_data = response.json()
    formatted = []

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

            formatted.append({
                "teams": teams,
                "time": time,
                "odds": odds_summary,
                "bookmaker": book.get("title", "N/A")
            })

    return jsonify({"games": formatted})

# Run the app locally
if __name__ == "__main__":
    app.run(debug=True)
