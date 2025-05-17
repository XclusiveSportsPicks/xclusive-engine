def calculate_units(confidence, odds):
    if odds > 0:
        b = odds / 100
    else:
        b = 100 / abs(odds)
    p = confidence / 10.0
    q = 1 - p
    try:
        kelly_fraction = (b * p - q) / b
        kelly_fraction = max(0, kelly_fraction)
    except ZeroDivisionError:
        kelly_fraction = 0
    return round(kelly_fraction * 0.5 * 10, 2)