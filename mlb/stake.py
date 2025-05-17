# mlb/stake.py

"""
Handles stake sizing logic using the Kelly Criterion (conservative 50% model).
Used to calculate unit exposure for each approved MLB pick.
"""

def calculate_kelly_stake(prob, odds, bankroll=100, kelly_fraction=0.5):
    """
    Calculates stake size using the Kelly Criterion.
    :param prob: win probability (e.g., 0.57)
    :param odds: American odds (e.g., -120, +135)
    :param bankroll: total bankroll (default 100)
    :param kelly_fraction: how much of the Kelly recommendation to bet
    :return: stake in units (rounded to 2 decimal places)
    """
    if odds > 0:
        decimal_odds = (odds / 100) + 1
    else:
        decimal_odds = (100 / abs(odds)) + 1

    b = decimal_odds - 1
    q = 1 - prob

    numerator = (b * prob) - q
    denominator = b

    kelly = numerator / denominator if denominator != 0 else 0
    kelly *= kelly_fraction
    stake = max(0, round(bankroll * kelly / 100, 2))
    return stake
