# mlb/engine.py
# Source: Combines ESPN matchups + OddsAPI + ML models
# Purpose: Generate elite MLB picks using Xclusive rules

from mlb.matchup import get_today_matchups
from mlb.odds import fetch_latest_odds
from mlb.stake import calculate_kelly_stake
from mlb.why_ilike import generate_why_i_like
from ml_models.mlb_confidence import predict_confidence
from ml_models.sharp_filter import get_sharp_delta

from datetime import datetime

SHARP_THRESHOLD = 30  # % difference between money % and bet %
CONFIDENCE_THRESHOLD = 7.5  # min score to be considered elite

def get_today_mlb_picks():
    picks = []
    matchups = get_today_matchups()

    for game in matchups:
        matchup = game["matchup"]
        pitchers = game["pitchers"]

        confidence = predict_confidence(matchup, pitchers)
        if confidence < CONFIDENCE_THRESHOLD:
            continue

        sharp_delta, sharp_meta = get_sharp_delta(matchup)
        if sharp_delta < SHARP_THRESHOLD:
            continue

        odds, movement = fetch_latest_odds(matchup)
        stake = calculate_kelly_stake(confidence, odds)
        why = generate_why_i_like(matchup, confidence, sharp_delta, movement)

        pick = {
            "matchup": matchup,
            "pitchers": pitchers,
            "confidence": round(confidence, 2),
            "sharp_delta": sharp_delta,
            "sharp_meta": sharp_meta,
            "odds": odds,
            "movement": movement,
            "stake": stake,
            "why": why,
            "status": "Pending",
            "result": None,
            "timestamp": datetime.utcnow().isoformat()
        }

        picks.append(pick)

    picks.sort(key=lambda p: p["confidence"], reverse=True)
    if picks:
        picks[0]["top_pick"] = True  # Flag the top one

    return picks
