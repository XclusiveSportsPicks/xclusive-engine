import requests
import os

def get_real_mlb_matchups():
    api_key = os.getenv("ODDS_API_KEY")
    if not api_key:
        print("❌ Missing ODDS_API_KEY")
        return []

    try:
        res = requests.get(
            "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds",
            params={
                "regions": "us",
                "markets": "h2h",
                "oddsFormat": "american",
                "apiKey": api_key
            }
        )
        res.raise_for_status()
        data = res.json()
        return [f"{game['teams'][0]} vs {game['teams'][1]}" for game in data]
    except Exception as e:
        print(f"❌ Error fetching matchups: {e}")
        return []
