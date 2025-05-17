# mlb/engine.py

from mlb.matchup import get_today_matchups
from mlb.odds import fetch_latest_odds
from mlb.stake import calculate_kelly_stake
from mlb.why_i_like import generate_reason
from ml_models.mlb_confidence import predict_confidence

def get_today_mlb_picks():
    matchups = get_today_matchups()
    picks = []

    for matchup in matchups:
        confidence = predict_confidence(matchup)
        if confidence < 7.5:
            continue

        odds, movement = fetch_latest_odds(matchup)
        if odds == -110.0:
            continue

        # Simulate sharp bet % data
        bet_pct = 40
        money_pct = 75
        sharp_delta = money_pct - bet_pct
        if sharp_delta < 30:
            continue

        stake = calculate_kelly_stake(confidence, odds)
        reason = generate_reason(matchup, confidence, odds, sharp_delta)

        picks.append({
            "matchup": matchup,
            "bet": "Moneyline",
            "confidence": round(confidence, 2),
            "sharp_delta": sharp_delta,
            "reason": reason,
            "odds": odds,
            "stake": stake,
            "movement": movement,
            "status": "Pending",
        })

    return sorted(picks, key=lambda x: x["confidence"], reverse=True)
