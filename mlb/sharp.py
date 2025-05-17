# mlb/sharp.py

import random

def fetch_sharp_percentages(matchup):
    """
    Mock function to simulate fetching sharp money percentage data.
    Replace with real sportsbook data logic if available.
    """
    # Simulated sharp values (you’ll need to replace with real data source)
    public_bet_pct = random.randint(30, 70)
    sharp_money_pct = public_bet_pct + random.randint(10, 35)

    sharp_delta = sharp_money_pct - public_bet_pct
    return sharp_money_pct, public_bet_pct, sharp_delta
