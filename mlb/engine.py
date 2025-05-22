from mlb.odds import get_odds_data
from mlb.model import rate_confidence_for_game
from mlb.sharp import get_sharp_data

def get_today_mlb_picks():
    games = get_odds_data()
    if not games:
        print("[❌ Engine] No games returned from OddsAPI.")
        return []

    sharp_data = get_sharp_data()
    picks = []
    skipped = 0

    for game in games:
        prediction = rate_confidence_for_game(game, sharp_data)

        if not isinstance(prediction, dict):
            print(f"[⚠️ Rejected] {game.get('home_team')} vs {game.get('away_team')} — Prediction not a dict.")
            skipped += 1
            continue

        required_fields = ["game", "pick", "confidence", "sharp_delta", "odds", "stake", "status", "why"]
        if not all(field in prediction and prediction[field] for field in required_fields):
            missing_fields = [f for f in required_fields if not prediction.get(f)]
            print(f"[⚠️ Incomplete] {prediction.get('game', 'Unknown')} — Missing fields: {missing_fields}")
            skipped += 1
            continue

        picks.append(prediction)

    print(f"[✅ Engine] Final picks: {len(picks)} / {len(games)}")
    if skipped:
        print(f"[ℹ️ Skipped] {skipped} games due to invalid or incomplete data.")
    return picks
