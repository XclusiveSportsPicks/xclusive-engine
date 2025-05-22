def predict_confidence(team_1, team_2, odds_1=0, odds_2=0, sharp_delta=0):
    base_confidence = 5.0
    if sharp_delta >= 30:
        base_confidence += 2.0
    if odds_1 > odds_2:
        base_confidence += 0.5
    return min(base_confidence, 10.0)
