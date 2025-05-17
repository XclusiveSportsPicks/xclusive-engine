# mlb/odds.py
# Source: Xclusive Sports Picks | Odds Fetch Module
# Licensed access to TheOddsAPI

import requests
import os

def fetch_latest_odds(matchup: str) -> tuple:
    """
    Fetch the latest H2H moneyline odds for a given MLB matchup.

    Args:
        matchup (str): Matchup string formatted as 'Away Team vs Home Team'

    Returns:
        tuple: (odds, odds_movement_label)
    """
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
