from .odds import fetch_latest_odds

def predict_confidence(away_team, home_team):
    matchup = f"{away_team} vs {home_team}"
    odds, movement = fetch_latest_odds(matchup)

    pitcher_edge = 0
    if "cole" in home_team.lower():
        pitcher_edge += 1.5
    if "degrom" in away_team.lower():
        pitcher_edge -= 1.0

    if odds < -120:
        odds_factor = 1.5
    elif odds < -110:
        odds_factor = 1.0
    elif odds < 100:
        odds_factor = 0.5
    else:
        odds_factor = 0.2

    if "Reverse" in movement:
        move_bonus = 1.0
    elif "Public" in movement:
        move_bonus = -0.5
    else:
        move_bonus = 0.0

    base_score = 6.0
    confidence = base_score + pitcher_edge + odds_factor + move_bonus

    return round(min(confidence, 10.0), 2)
