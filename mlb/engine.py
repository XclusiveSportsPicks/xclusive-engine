# mlb/engine.py

from mlb.matchup import get_today_matchups
from mlb.odds import fetch_latest_odds
from mlb.sharp import fetch_sharp_percentages
from mlb.stake import calculate_kelly_stake
from mlb.why_i_like import generate_why_i_like
from ml_models.mlb_confidence import predict_confidence

def get_today_mlb_picks():
    matchups = get_today_matchups()
    sharp_data = fetch_sharp_percentages()
    picks = []

    for matchup in matchups:
        confidence = predict_confidence(matchup)
        if confidence < 7.5:
            continue

        sharp = sharp_data.get(matchup, {"bet_pct": 0, "money_pct": 0})
        bet_pct = sharp.get("bet_pct", 0)
        money_pct = sharp.get("money_pct", 0)
        sharp_delta = money_pct - bet_pct

        if sharp_delta < 30:
            continue

        odds, movement = fetch_latest_odds(matchup)
        if odds is None:
            continue

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

    picks.sort(key=lambda x: x["confidence"], reverse=True)

    if picks:
        picks[0]["label"] = "Xs Absolute Best Bet"

    return picks
