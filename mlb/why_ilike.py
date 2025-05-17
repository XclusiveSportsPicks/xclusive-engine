# mlb/why_ilike.py

"""
Auto-generates a “Why I Like It” blurb based on pick metadata.
Used in Xclusive Sports Picks daily output.
"""

def generate_why_i_like(matchup, confidence, sharp_delta, odds, pitcher_note=""):
    lines = []

    if confidence >= 9:
        lines.append("Model LOVES this play with elite confidence.")
    elif confidence >= 8.5:
        lines.append("Strong model edge based on latest projections.")
    elif confidence >= 8:
        lines.append("Confident read backed by sharp signals.")
    else:
        lines.append("Slight model lean, but meets confidence filters.")

    if sharp_delta >= 40:
        lines.append("Massive sharp action discrepancy.")
    elif sharp_delta >= 30:
        lines.append("Sharp money is clearly on this side.")
    elif sharp_delta >= 20:
        lines.append("Some sharp interest detected.")

    if odds >= -130 and odds <= +120:
        lines.append("Fair odds with strong value potential.")
    elif odds > +120:
        lines.append("Underdog spot with high potential ROI.")
    elif odds < -140:
        lines.append("Juiced line but the model justifies it.")

    if pitcher_note:
        lines.append(f"Pitching note: {pitcher_note}")

    return " ".join(lines)
