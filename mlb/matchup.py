# mlb/matchup.py

from mlb.odds import fetch_latest_odds
from mlb.why_ilike import generate_why_i_like
from mlb.stake import calculate_kelly_stake
from mlb.models import predict_confidence
from datetime import datetime

def get_today_matchups():
    # Placeholder — in production, pull from ESPN/Flashscore
    return [
        {
            "matchup": "Yankees vs Red Sox",
            "date": datetime.utcnow().strftime("%Y-%m-%d")
        },
        {
            "matchup": "Dodgers vs Giants",
            "date": datetime.utcnow().strftime("%Y-%m-%d")
        }
    ]

def enrich_matchup_data(raw_matchups):
    picks = []
    for match in raw_matchups:
        confidence = predict_confidence(match["matchup"])
        if confidence < 7.5:
            continue

        odds, odds_note = fetch_latest_odds(match["matchup"])
        stake = calculate_kelly_stake(confidence, odds)
        why = generate_why_i_like(match["matchup"])

        picks.append({
            "matchup": match["matchup"],
            "confidence": confidence,
            "odds": odds,
            "odds_note": odds_note,
            "stake": stake,
            "why": why,
            "date": match["date"]
        })
    return picks
