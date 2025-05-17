# mlb/engine.py

from mlb.matchup import get_today_matchups
from mlb.odds import fetch_latest_odds
from mlb.sharp import fetch_sharp_percentages
from mlb.stake import calculate_kelly_stake
from mlb.why_i_like import generate_why_i_like
from ml_models.mlb_confidence import predict_confidence
from datetime import datetime

def get_today_mlb_picks():
    matchups = get_today_matchups()
    sharp_data = fetch_sharp_percentages()

    picks = []

    for matchup in matchups:
        # Use the string version for all data mapping
        matchup_str = matchup["matchup"] if isinstance(matchup, dict) else matchup
        confidence = predict_confidence(matchup)

        if confidence < 7.5:
            continue

        sharp = sharp_data.get(matchup_str, {"bet_pct": 0, "money_pct": 0})
        sharp_delta = sharp["money_pct"] - sharp["bet_pct"]

        if sharp_delta < 30:
            continue

        odds, movement = fetch_latest_odds(matchup_str)
        stake = calculate_kelly_stake(confidence, odds)

        pick = {
            "matchup": matchup_str,
            "confidence": round(confidence, 2),
            "sharp_delta": sharp_delta,
            "odds": odds,
            "movement": movement,
            "stake": stake,
            "why": generate_why_i_like(matchup_str, confidence, sharp_delta),
            "status": "Pending",
            "result": None,
        }

        picks.append(pick)

    picks.sort(key=lambda x: x["confidence"], reverse=True)

    if picks:
        picks[0]["label"] = "Xs Absolute Best Bet"

    return picks
