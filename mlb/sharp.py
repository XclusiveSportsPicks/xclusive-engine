# mlb/sharp.py

import requests
import os

def fetch_sharp_percentages():
    api_key = os.getenv("ODDS_API_KEY")
    url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds?apiKey={api_key}&regions=us&markets=h2h&oddsFormat=decimal"

    try:
        response = requests.get(url)
        response.raise_for_status()
        games = response.json()
    except Exception as e:
        print(f"[❌ SharpAPI] Failed to fetch odds data: {e}")
        return {}

    sharp_data = {}

    for game in games:
        teams = game.get("teams", [])
        if len(teams) != 2:
            continue

        home_team = game.get("home_team")
        away_team = [team for team in teams if team != home_team][0]
        matchup = f"{away_team} vs {home_team}"

        for site in game.get("bookmakers", []):
            for market in site.get("markets", []):
                if market["key"] == "h2h":
                    outcomes = market["outcomes"]
                    if len(outcomes) != 2:
                        continue

                    bet_data = {
                        outcome["name"]: {
                            "bet_pct": outcome.get("bet_percentage", 0),
                            "money_pct": outcome.get("money_percentage", 0),
                        }
                        for outcome in outcomes
                    }

                    away_data = bet_data.get(away_team, {"bet_pct": 0, "money_pct": 0})
                    sharp_data[matchup] = away_data
                    break  # Found h2h market, move to next game
            break  # One bookmaker is enough
    return sharp_data
