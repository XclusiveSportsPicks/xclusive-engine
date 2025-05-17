# mlb/engine.py

from datetime import datetime
from mlb.matchup import get_today_matchups
from mlb.odds import load_odds_once, fetch_latest_odds
from mlb.sharp import fetch_sharp_percentages
from mlb.stake import calculate_kelly_stake
from mlb.why_i_like import generate_why_i_like
from ml_models.mlb_confidence import predict_confidence

def get_today_mlb_picks():
    matchups = get_today_matchups()
    sharp_data = fetch_sharp_percentages()
    load_odds_once()  # Only fetch odds once and cache

    picks = []

    for matchup in matchups:
        confidence = predict_confidence(matchup)
        if confidence < 7.5:
            continue

        sharp = sharp_data.get(matchup, {"bet_pct": 0, "money_pct": 0})
        bet_pct = sharp["bet_pct"]
        money_pct = sharp["money_pct"]
        sharp_delta = money_pct - bet_pct

        if sharp_delta < 30:
            continue

        odds, movement = fetch_latest_odds(matchup)
        stake = calculate_kelly_stake(confidence, odds)

        pick = {
            "matchup": matchup,
            "confidence": round(confidence, 2),
            "sharp_delta": sharp_delta,
            "odds": odds,
            "movement": movement,
            "stake": stake,
            "why": generate_why_i_like(matchup, confidence, sharp_delta),
            "status": "Pending",
            "result": None,
        }

        picks.append(pick)

    # Sort by confidence descending
    picks.sort(key=lambda x: x["confidence"], reverse=True)

    # Flag top pick
    if picks:
        picks[0]["label"] = "Xs Absolute Best Bet"

    return picks
