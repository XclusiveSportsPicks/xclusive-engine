import requests
import os

def fetch_latest_odds(matchup):
    api_key = os.getenv("ODDS_API_KEY")
    if not api_key:
        print("[Odds ❌] No API key found")
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
            if home in teams and away in teams:
                outcomes = game.get("bookmakers", [])[0]["markets"][0]["outcomes"]
                for outcome in outcomes:
                    if outcome["name"] == home:
                        odds = outcome["price"]
                        return odds, "— No Movement"  # You can later improve movement logic
                break

        print(f"[Odds ❌] Matchup not found: {matchup}")
        return -110.0, "— Not Found"

    except Exception as e:
        print(f"[OddsAPI ❌] Error: {e}")
        return -110.0, "— API Error"
