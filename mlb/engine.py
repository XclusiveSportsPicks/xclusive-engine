# mlb/engine.py

import sys
import os
from datetime import datetime

# Ensure parent dir is importable
PARENT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PARENT not in sys.path:
    sys.path.append(PARENT)

from .pitching import get_pitcher_stats
from ..odds_fetch import get_real_mlb_matchups
from ..ml_models.mlb_confidence import predict_confidence
from ..stake_calc import calculate_stake
from ..why_i_like_it import generate_blurb


def get_today_mlb_picks():
    matchups = get_real_mlb_matchups()
    print("📡 Pulled Matchups:", len(matchups))

    today_str = datetime.now().strftime('%Y-%m-%d')
    picks = []

    for matchup in matchups:
        try:
            teams = matchup.get("teams", [])
            game_date = matchup.get("date", today_str)

            if not teams or len(teams) != 2:
                print("⛔ Invalid team format:", matchup)
                continue

            if game_date != today_str:
                print("⏭️ Skipping non-today game:", game_date)
                continue

            money_pct = matchup.get("money_pct")
            bet_pct = matchup.get("bet_pct")

            if money_pct is None or bet_pct is None:
                print("⛔ Missing sharp data:", matchup)
                continue

            sharp_delta = money_pct - bet_pct
            confidence = predict_confidence(teams[0], teams[1]) * 10  # out of 10

            print(f"🧠 {teams} | Conf: {confidence:.2f}, Sharp Δ: {sharp_delta}")

            if confidence < 7.5 or sharp_delta < 30:
                continue

            pick = {
                "game": f"{teams[0]} vs {teams[1]}",
                "pick": matchup.get("recommended_pick", "N/A"),
                "odds": matchup.get("odds", "N/A"),
                "confidence": round(confidence, 2),
                "sharp_percent": sharp_delta,
                "stake": calculate_stake(confidence),
                "status": "In Progress",
                "result": "TBD",
                "why": generate_blurb(matchup),
                "timestamp": datetime.now().isoformat()
            }

            picks.append(pick)

        except Exception as e:
            print("⚠️ Matchup Processing Error:", e)

    if picks:
        picks.sort(key=lambda x: x["confidence"], reverse=True)
        picks[0]["best_bet"] = True  # Mark highest-confidence pick

    return picks
