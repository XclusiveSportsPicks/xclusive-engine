# mlb/why_like.py

def generate_blurb(game):
    """
    Generates a compact, data-backed betting insight blurb.
    Input: dict with keys 'pitchers', 'sharp_percent', 'confidence', 'injuries'
    Output: concise string reason
    """
    pitchers = game.get("pitchers", {})
    injuries = game.get("injuries", {})
    confidence = game.get("confidence", 0.0)
    sharp_percent = game.get("sharp_percent", 0)

    away_pitcher = pitchers.get("away_pitcher", "Unknown")
    home_pitcher = pitchers.get("home_pitcher", "Unknown")

    lines = []

    # Pitching signal
    if "unknown" not in (away_pitcher.lower(), home_pitcher.lower()):
        lines.append(f"{home_pitcher} vs {away_pitcher} sets up a key pitching edge.")

    # Sharp money
    if sharp_percent >= 30:
        lines.append("Heavy sharp action (Δ ≥ 30%) supporting this side.")

    # Confidence signal
    if confidence >= 8.5:
        lines.append("Model shows high confidence based on matchup analytics.")

    # Injury insights
    injury_notes = []
    if injuries.get("home_key_player_out"):
        injury_notes.append("key home player OUT")
    if injuries.get("away_key_player_out"):
        injury_notes.append("key away player OUT")
    if injury_notes:
        lines.append("Injury Watch: " + ", ".join(injury_notes).capitalize() + ".")

    return " ".join(lines) if lines else "Smart alignment between model confidence and sharp market activity."
