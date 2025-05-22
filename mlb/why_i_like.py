def generate_why_i_like(matchup, confidence, sharp_delta, pitchers=None, injuries=None):
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

    if pitchers:
        reasons.append(f"🧤 Pitchers: {pitchers['away_pitcher']} vs {pitchers['home_pitcher']}")

    if injuries:
        if injuries.get("away_key_player_out"):
            reasons.append("🚑 Key injury concern on the away side.")
        if injuries.get("home_key_player_out"):
            reasons.append("🚑 Home team has injury red flag.")

    return " ".join(reasons)
