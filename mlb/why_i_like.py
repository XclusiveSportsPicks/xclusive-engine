# mlb/why_i_like.py

def generate_why_i_like(matchup, confidence, sharp_delta):
    """
    Generates a quick blurb explaining why this pick is being recommended.
    """
    reasons = []

    if confidence >= 9:
        reasons.append("🔥 Our model shows extreme confidence in this matchup.")
    elif confidence >= 8:
        reasons.append("✅ Model signals strong edge here.")
    elif confidence >= 7.5:
        reasons.append("💡 This play meets the threshold for confidence.")

    if sharp_delta >= 35:
        reasons.append("📈 Heavy sharp money discrepancy detected.")
    elif sharp_delta >= 30:
        reasons.append("💸 Solid sharp action vs public betting.")

    if "vs" in matchup:
        away, home = matchup.split(" vs ")
        reasons.append(f"📊 {away} vs {home} profile fits elite criteria.")

    return " ".join(reasons)

