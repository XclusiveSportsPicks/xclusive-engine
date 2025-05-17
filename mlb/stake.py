# mlb/stake.py

def calculate_stake(confidence, odds=-110):
    """
    Calculates stake units using 50% Kelly Criterion
    Input:
        - confidence: float (7.5–10.0 range, normalized to 0–1)
        - odds: American format (e.g. -110, +120)
    Output:
        - stake_units: float (0–5.0 scale)
    """
    try:
        # Convert odds to b (net profit per unit)
        b = odds / 100.0 if odds > 0 else 100.0 / abs(odds)
        p = confidence / 10.0
        q = 1.0 - p

        kelly = (b * p - q) / b
        stake_units = max(0, kelly * 0.5 * 10)  # 50% Kelly, 10-unit scale

        return round(stake_units, 2)

    except Exception as e:
        print(f"[⚠️ Stake Calc Error] {e}")
        return 0.0
