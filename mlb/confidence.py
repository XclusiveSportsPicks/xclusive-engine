# mlb/confidence.py

from .odds import fetch_latest_odds

def predict_confidence(away_team, home_team):
    matchup = f"{away_team} vs {home_team}"
    odds, movement = fetch_latest_odds(matchup)

    # 💪 Placeholder pitcher logic (can upgrade later with ERA/K/WHIP)
    pitcher_edge = 0
    if "cole" in home_team.lower():
        pitcher_edge += 1.2
    if "degrom" in away_team.lower():
        pitcher_edge -= 1.0

    # 💰 Odds tiers
    if odds <= -150:
        odds_factor = 1.75
    elif odds <= -120:
        odds_factor = 1.25
    elif odds < -100:
        odds_factor = 0.75
    elif odds < +120:
        odds_factor = 0.3
    else:
        odds_factor = 0.1

    # 📈 Line movement weight
    move_bonus = 0
    if "Reverse" in movement:
        move_bonus = 1.0
    elif "Steam" in movement:
        move_bonus = 0.5
    elif "Public" in movement:
        move_bonus = -0.5

    # 🧠 Base model score
    base_score = 6.0
    confidence = base_score + pitcher_edge + odds_factor + move_bonus

    return round(min(confidence, 10.0), 2)
