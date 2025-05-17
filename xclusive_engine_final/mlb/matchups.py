import requests
import os

def get_real_mlb_matchups():
    api_key = os.getenv("ODDS_API_KEY")
    if not api_key:
        print("[Matchups ❌] Missing ODDS_API_KEY in environment")
        return []

    try:
        url = "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"
        params = {
            "regions": "us",
            "markets": "h2h",
            "oddsFormat": "american",
            "apiKey": api_key
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        games = response.json()

        matchups = []
        for game in games:
            teams = game.get("teams", [])
            bookmakers = game.get("bookmakers", [])
            if len(teams) != 2 or not bookmakers:
                continue

            home_team = game.get("home_team")
            away_team = [team for team in teams if team != home_team][0]
            matchup = f"{away_team} vs {home_team}"

            # Simulate bet/money % — replace with real if available from another provider
            bet_pct = 40
            money_pct = 75

            matchups.append({
                "matchup": matchup,
                "bet_pct": bet_pct,
                "money_pct": money_pct
            })

        return matchups

    except Exception as e:
        print(f"[Matchups ❌] Error fetching matchups: {e}")
        return []
