
# mlb/odds.py
# Source: Xclusive Sports Picks | Odds Fetch Module

import requests
import os

# Global in-memory cache
ODDS_CACHE = {}

def load_odds_once():
    """
    Fetch odds data once per session and store it in memory.
    """
    global ODDS_CACHE

    api_key = os.getenv("0872bbfe3e80dddd635a1f6d21b09201")
    if not api_key:
        print("[❌ OddsAPI] Missing API key")
        return

    try:
        response = requests.get(
            "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds",
            params={
                "apiKey": api_key,
                "regions": "us",
                "markets": "h2h",
                "oddsFormat": "american"
            }
        )
        response.raise_for_status()
        ODDS_CACHE["games"] = response.json()
        print(f"[✅ OddsAPI] Fetched {len(ODDS_CACHE['games'])} games")
    except Exception as e:
        print(f"[❌ OddsAPI] Error loading odds: {e}")
        ODDS_CACHE["games"] = []

def fetch_latest_odds(matchup):
    """
    Lookup odds from cached data for a given matchup.
    Returns tuple: (odds, label)
    """
    if "games" not in ODDS_CACHE:
        print("[⚠️ OddsAPI] Odds data not loaded. Run load_odds_once() first.")
        return -110.0, "— Not Loaded"

    away, home = matchup.split(" vs ")

    for game in ODDS_CACHE["games"]:
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
