# mlb/mlb_schedule.py

import requests

def fetch_today_games():
    """
    Returns list of today's MLB matchups as 'Away vs Home' strings.
    Source: ESPN public MLB scoreboard API
    """
    url = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        games = data.get("events", [])

        today_matchups = []

        for game in games:
            comps = game.get("competitions", [])
            if not comps:
                continue

            teams = comps[0].get("competitors", [])
            if len(teams) != 2:
                continue

            home = next((t for t in teams if t.get("homeAway") == "home"), {}).get("team", {}).get("displayName")
            away = next((t for t in teams if t.get("homeAway") == "away"), {}).get("team", {}).get("displayName")

            if home and away:
                today_matchups.append(f"{away} vs {home}")

        return today_matchups

    except Exception as e:
        print(f"[❌ MLB Schedule] Failed to fetch games: {e}")
        return []
