# mlb/odds_fetch.py

import requests
import os

def get_real_mlb_matchups():
    api_key = os.getenv("ODDS_API_KEY")
    if not api_key:
        print("[❌ OddsAPI] Missing API key")
        return []

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

        matchups = []
        for game in data:
            teams = game.get("teams", [])
            if len(teams) == 2:
                away, home = teams
                matchup = f"{away} vs {home}"
                matchups.append(matchup)

        return matchups

    except Exception as e:
        print(f"[❌ OddsAPI] Error fetching matchups: {e}")
        return []
