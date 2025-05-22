# odds.py
import requests
import os

ODDS_API_KEY = os.getenv("ODDS_API_KEY")
ODDS_API_URL = "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"

def fetch_live_odds():
    params = {
        "regions": "us",
        "markets": "h2h",
        "oddsFormat": "american",
        "apiKey": ODDS_API_KEY
    }
    res = requests.get(ODDS_API_URL, params=params)
    res.raise_for_status()
    return res.json()
