def calculate_kelly_stake(confidence, odds):
    probability = confidence / 10
    decimal_odds = (100 + abs(odds)) / abs(odds) if odds < 0 else (odds / 100) + 1
    edge = (decimal_odds * probability) - 1
    kelly = edge / (decimal_odds - 1)
    stake = max(0, min(kelly * 100 * 0.5, 100))  # Half Kelly, capped at 100
    return round(stake, 2)
