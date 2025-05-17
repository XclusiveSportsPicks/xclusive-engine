# mlb/sharp.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_sharp_percentages():
    api_key = os.getenv("ODDS_API_KEY")
    url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds?regions=us&markets=spreads&apiKey={api_key}"

    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        print(f"[❌ Sharp %] Failed to load: {e}")
        return {}

    sharp_data = {}

    for game in data:
        teams = game.get("teams", [])
        if len(teams) != 2:
            continue

        home_team = game.get("home_team")
        away_team = [t for t in teams if t != home_team][0]
        matchup = f"{away_team} vs {home_team}"

        sites = game.get("bookmakers", [])
        for site in sites:
            if site["title"] == "DraftKings":
                markets = site.get("markets", [])
                for market in markets:
                    outcomes = market.get("outcomes", [])
                    if len(outcomes) >= 2:
                        sharp_data[matchup] = {
                            "bet_pct": 30 + hash(matchup) % 40,    # Simulated
                            "money_pct": 60 + hash(matchup[::-1]) % 40
                        }
                break

    return sharp_data
