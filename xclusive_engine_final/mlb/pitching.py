# mlb/pitching.py

import requests
from bs4 import BeautifulSoup

def get_pitcher_stats(game_str):
    """
    Scrapes probable pitchers for a given game from ESPN.
    Expects game_str like "Yankees vs Red Sox"
    Returns dict with away and home pitcher names.
    """
    url = "https://www.espn.com/mlb/schedule"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        away_team, home_team = [team.strip().lower() for team in game_str.split("vs")]

        for row in soup.select("table tbody tr"):
            teams = row.select("td a")
            pitcher_cells = row.select("td")

            if len(teams) >= 2 and len(pitcher_cells) >= 5:
                away = teams[0].text.strip().lower()
                home = teams[1].text.strip().lower()

                if away_team in away and home_team in home:
                    away_pitcher = pitcher_cells[2].text.strip() or "Unknown"
                    home_pitcher = pitcher_cells[3].text.strip() or "Unknown"

                    return {
                        "away_pitcher": away_pitcher,
                        "home_pitcher": home_pitcher
                    }

    except Exception as e:
        print(f"[Pitching Error] {e}")

    return {"away_pitcher": "Unknown", "home_pitcher": "Unknown"}
