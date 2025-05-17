# mlb/odds.py

import requests
import os

def fetch_latest_odds(matchup):
    api_key = os.getenv("ODDS_API_KEY")
    if not api_key:
        print("[❌ OddsAPI] Missing API key")
        return -110.0, "— No Key"

    try:
        response = requests.get(
            "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds",
            params={
                "regions": "us",
                "markets": "h2h",
                "oddsFormat": "american",
                "apiKey": api_key
            }
        )
        response.raise_for_status()
        data = response.json()

        away, home = matchup.split(" vs ")

        for game in data:
            teams = game.get("teams", [])
            if not teams or home not in teams or away not in teams:
                continue

            bookmakers = game.get("bookmakers", [])
            if not bookmakers:
                continue

            markets = bookmakers[0].get("markets", [])
            if not markets:
                continue

            outcomes = markets[0].get("outcomes", [])
            for outcome in outcomes:
                if outcome["name"] == home:
                    odds = outcome["price"]
                    return odds, "Neutral"

        print(f"[❌ OddsAPI] Matchup not found: {matchup}")
        return -110.0, "— Not Found"

    except Exception as e:
        print(f"[❌ OddsAPI] Error during fetch: {e}")
        return -110.0, "— API Error"
