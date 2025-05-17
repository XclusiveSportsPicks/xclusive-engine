import requests
from datetime import datetime

def fetch_today_games():
    """
    Returns a list of matchup strings like 'Team A vs Team B' for today's MLB games.
    """
    url = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        games = data.get("events", [])
        today_matchups = []

        for game in games:
            competitions = game.get("competitions", [])
            if not competitions:
                continue

            teams = competitions[0].get("competitors", [])
            if len(teams) != 2:
                continue

            home = next((t for t in teams if t.get("homeAway") == "home"), {}).get("team", {}).get("displayName")
            away = next((t for t in teams if t.get("homeAway") == "away"), {}).get("team", {}).get("displayName")

            if home and away:
                today_matchups.append(f"{away} vs {home}")

        return today_matchups

    except Exception as e:
        print(f"[MLB Schedule ❌] Failed to fetch games: {e}")
        return []
