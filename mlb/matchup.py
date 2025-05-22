# mlb/matchup.py

import requests
from mlb.why_i_like import generate_why_i_like
from mlb.odds import fetch_latest_odds
from mlb.stake import calculate_kelly_stake
from datetime import datetime

ESPN_SCHEDULE_URL = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"

def get_today_matchups():
    try:
        response = requests.get(ESPN_SCHEDULE_URL)
        response.raise_for_status()
        data = response.json()

        games = data.get("events", [])
        matchups = []

        for game in games:
            competitions = game.get("competitions", [])
            if not competitions:
                continue

            competition = competitions[0]
            competitors = competition.get("competitors", [])
            if len(competitors) != 2:
                continue

            home = next((c for c in competitors if c["homeAway"] == "home"), None)
            away = next((c for c in competitors if c["homeAway"] == "away"), None)
            if not home or not away:
                continue

            home_team = home["team"]["displayName"]
            away_team = away["team"]["displayName"]
            matchup = f"{away_team} vs {home_team}"

            odds, odds_note = fetch_latest_odds(matchup)
            confidence = 7.8  # placeholder
            sharp_delta = 32  # placeholder
            stake = calculate_kelly_stake(confidence, odds)
            why = generate_why_i_like(matchup, confidence, sharp_delta)

            matchups.append({
                "matchup": matchup,
                "confidence": confidence,
                "sharp_delta": sharp_delta,
                "why": why,
                "odds": odds,
                "stake": stake,
                "note": odds_note,
                "status": "PENDING",
                "result": "TBD"
            })

        return matchups

    except Exception as e:
        print(f"[❌ ESPN Fetch Error] {e}")
        return []
