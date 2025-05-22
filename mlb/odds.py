import requests
import os

ODDS_API_KEY = os.getenv("ODDS_API_KEY")

def get_odds_data():
    url = "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"
    params = {
        "regions": "us",
        "markets": "h2h",
        "oddsFormat": "american",
        "apiKey": ODDS_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        games = response.json()
    except Exception as e:
        print("[ERROR] Failed to fetch odds:", str(e))
        return []

    odds_data = []
    for game in games:
        if not game.get("bookmakers"):
            continue

        bookmaker = game["bookmakers"][0]
        markets = bookmaker.get("markets", [])
        if not markets or not markets[0].get("outcomes"):
            continue

        outcomes = markets[0]["outcomes"]
        if len(outcomes) < 2:
            continue

        odds_data.append({
            "team1": outcomes[0]["name"],
            "team2": outcomes[1]["name"],
            "odds1": outcomes[0]["price"]
        })

    return odds_data
