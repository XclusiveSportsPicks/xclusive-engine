import datetime
from ml_models.mlb_confidence import predict_confidence
from mlb.odds import fetch_latest_odds
from mlb.matchup import get_matchups_today
from mlb.stake import calculate_kelly_stake
from mlb.why_i_like import generate_reason

def get_today_mlb_picks():
    matchups = get_matchups_today()
    if not matchups:
        print("[❌ Engine] No MLB matchups found.")
        return []

    picks = []
    for matchup in matchups:
        confidence = predict_confidence(matchup)
        if confidence < 7.5:
            continue

        odds, movement = fetch_latest_odds(matchup)
        sharp_delta = 35  # Placeholder; replace with real logic later
        if sharp_delta < 30:
            continue

        stake = calculate_kelly_stake(confidence, odds)
        reason = generate_reason(matchup, confidence, odds, sharp_delta)

        pick = {
            "game": matchup,
            "bet": "Moneyline",
            "confidence": round(confidence, 2),
            "sharp_delta": sharp_delta,
            "why": reason,
            "odds": odds,
            "stake": stake,
            "status": "PENDING",
            "result": None,
        }
        picks.append(pick)

    # Sort by highest confidence
    picks.sort(key=lambda x: x["confidence"], reverse=True)

    if picks:
        picks[0]["best_bet"] = True

    return picks
