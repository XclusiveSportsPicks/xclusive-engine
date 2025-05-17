# mlb/pitching.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_pitcher_stats(game_str):
    """
    Scrapes today's probable pitchers for a given game from ESPN.
    Input: "Yankees vs Red Sox"
    Output: {"away_pitcher": "...", "home_pitcher": "..."}
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

        today_str = datetime.now().strftime('%A, %B %-d')
        away_team, home_team = [t.strip().lower() for t in game_str.split("vs")]

        for section in soup.select("section.ScheduleTables"):
            if today_str not in section.text:
                continue

            for row in section.select("table tbody tr"):
                team_links = row.select("td a")
                tds = row.select("td")

                if len(team_links) >= 2 and len(tds) >= 5:
                    away = team_links[0].text.strip().lower()
                    home = team_links[1].text.strip().lower()

                    if away_team in away and home_team in home:
                        # Pitchers should be in 3rd and 4th cells
                        away_pitcher = tds[2].text.strip() or "Unknown"
                        home_pitcher = tds[3].text.strip() or "Unknown"

                        return {
                            "away_pitcher": away_pitcher,
                            "home_pitcher": home_pitcher
                        }

    except Exception as e:
        print(f"[⚠️ Pitching Scrape Error] {e}")

    return {"away_pitcher": "Unknown", "home_pitcher": "Unknown"}
