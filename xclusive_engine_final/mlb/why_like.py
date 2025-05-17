def generate_why_i_like_it_blurb(game):
    """
    Builds a data-backed reasoning string based on sharp %, confidence, pitcher edge, and injuries.
    Expects game dict with keys: 'pitchers', 'sharp_percent', 'confidence', 'injuries'
    """
    pitchers = game.get("pitchers", {})
    injuries = game.get("injuries", {})
    confidence = game.get("confidence", 0.0)

    away_pitcher = pitchers.get("away_pitcher", "Unknown")
    home_pitcher = pitchers.get("home_pitcher", "Unknown")

    lines = []

    # Pitching angle
    if "Unknown" not in (away_pitcher, home_pitcher):
        lines.append(f"{home_pitcher} is starting against {away_pitcher} — pitching edge aligns with the model.")

    # Sharp Money
    sharp_percent = game.get("sharp_delta", 0)
    if sharp_percent >= 30:
        lines.append("Significant sharp money detected (Sharp Delta ≥ 30%).")

    # Confidence
    if confidence >= 8.5:
        lines.append("High model confidence due to team momentum and matchup analytics.")

    # Injury insights
    if injuries:
        notes = []
        if injuries.get("home_key_player_out"):
            notes.append("key player OUT for home team")
        if injuries.get("away_key_player_out"):
            notes.append("key player OUT for away team")
        if notes:
            lines.append("Injury Watch: " + ", ".join(notes).capitalize() + ".")

    return " ".join(lines) if lines else "Solid alignment between sharp action and model signals."
