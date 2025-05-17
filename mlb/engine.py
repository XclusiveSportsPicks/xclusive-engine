# mlb/engine.py

from mlb.matchup import get_today_matchups
from mlb.odds import fetch_latest_odds, load_odds_once
from mlb.sharp import fetch_sharp_percentages
from mlb.stake import calculate_kelly_stake
from mlb.why_i_like import generate_why_i_like
from ml_models.mlb_confidence import predict_confidence
from datetime import datetime

def get_today_mlb_picks():
    matchups = get_today_matchups()
    load_odds_once()  # 💡 Load odds once to avoid repeated API hits
    picks = []

    for matchup_data in matchups:
        # Support both string or dict style
        if isinstance(matchup_data, dict):
            matchup = matchup_data.get("matchup", "")
        else:
            matchup = matchup_data

        if not matchup or not isinstance(matchup, str):
            print(f"[❌ Skipping] Invalid matchup: {matchup_data}")
            continue

        confidence = predict_confidence(matchup)
        if confidence < 7.5:
            continue

        sharp = fetch_sharp_percentages(matchup)
        bet_pct = sharp.get("bet_pct", 0)
        money_pct = sharp.get("money_pct", 0)
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

    picks.sort(key=lambda x: x["confidence"], reverse=True)

    if picks:
        picks[0]["label"] = "Xs Absolute Best Bet"

    return picks
