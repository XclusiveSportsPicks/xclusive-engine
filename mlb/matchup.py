# mlb/matchup.py
# Source: ESPN.com MLB Scoreboard Page (public info)
# Usage: For public display and analysis, not for redistribution
# Attribution required: "Data from ESPN.com"

import requests
from bs4 import BeautifulSoup
from datetime import datetime

ESPN_SCOREBOARD_URL = "https://www.espn.com/mlb/scoreboard"

def get_today_matchups():
    try:
        response = requests.get(ESPN_SCOREBOARD_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        matchups = []

        scoreboard = soup.select('section.Scoreboard')
        today_str = datetime.utcnow().strftime("%A, %B %d")

        for game in scoreboard:
            teams = game.select('.ScoreCell__TeamName')
            pitchers = game.select('.ScoreCell__Pitcher')

            if len(teams) == 2:
                away_team = teams[0].get_text(strip=True)
                home_team = teams[1].get_text(strip=True)
                matchup_str = f"{away_team} vs {home_team}"

                away_pitcher = pitchers[0].get_text(strip=True) if len(pitchers) > 1 else "TBD"
                home_pitcher = pitchers[1].get_text(strip=True) if len(pitchers) > 1 else "TBD"
                pitcher_str = f"{away_pitcher} @ {home_pitcher}"

                matchups.append({
                    "matchup": matchup_str,
                    "pitchers": pitcher_str,
                    "date": today_str
                })

        return matchups

    except Exception as e:
        print(f"[❌ ESPN] Error fetching matchups: {e}")
        return []
