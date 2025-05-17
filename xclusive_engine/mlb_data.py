# mlb/mlb_data.py

import requests
from bs4 import BeautifulSoup

PITCHER_URL = "https://www.rotowire.com/baseball/daily-lineups.php"
INJURY_URL = "https://www.rotowire.com/baseball/injury-report.php"

def scrape_pitchers():
    try:
        res = requests.get(PITCHER_URL, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        games = soup.find_all("div", class_="lineup")
        pitcher_map = {}

        for game in games:
            teams = game.find_all("div", class_="lineup__team")
            if len(teams) < 2:
                continue

            away_team = teams[0].find("span", class_="lineup__abbr").text.strip()
            home_team = teams[1].find("span", class_="lineup__abbr").text.strip()
            away_pitcher = teams[0].find("span", class_="lineup__player").text.strip()
            home_pitcher = teams[1].find("span", class_="lineup__player").text.strip()

            matchup = f"{away_team} vs {home_team}"
            pitcher_map[matchup] = {
                "away_pitcher": away_pitcher,
                "home_pitcher": home_pitcher
            }

        return pitcher_map

    except Exception as e:
        print(f"[Pitcher Scrape Error] {e}")
        return {}


def scrape_injuries():
    try:
        res = requests.get(INJURY_URL, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        table = soup.find("table", class_="tablesorter")
        rows = table.find_all("tr")[1:]

        injuries = {}
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 5:
                continue

            team = cols[0].text.strip().lower()
            player = cols[1].text.strip()
            status = cols[4].text.strip()

            injuries.setdefault(team, []).append(f"{player} - {status}")

        return injuries

    except Exception as e:
        print(f"[Injury Scrape Error] {e}")
        return {}


def get_today_mlb_data():
    pitchers = scrape_pitchers()
    injuries = scrape_injuries()
    mlb_data = {}

    for matchup, pitch_data in pitchers.items():
        away, home = matchup.split(" vs ")
        away_key = away.lower()
        home_key = home.lower()

        mlb_data[matchup] = {
            "pitchers": pitch_data,
            "injuries": {
                "away_key_player_out": bool(injuries.get(away_key)),
                "home_key_player_out": bool(injuries.get(home_key))
            }
        }

    return mlb_data
