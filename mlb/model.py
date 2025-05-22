TEAM_ABBREVIATIONS = {
    "Arizona Diamondbacks": "ARI",
    "Atlanta Braves": "ATL",
    "Baltimore Orioles": "BAL",
    "Boston Red Sox": "BOS",
    "Chicago Cubs": "CHC",
    "Chicago White Sox": "CWS",
    "Cincinnati Reds": "CIN",
    "Cleveland Guardians": "CLE",
    "Colorado Rockies": "COL",
    "Detroit Tigers": "DET",
    "Houston Astros": "HOU",
    "Kansas City Royals": "KC",
    "Los Angeles Angels": "LAA",
    "Los Angeles Dodgers": "LAD",
    "Miami Marlins": "MIA",
    "Milwaukee Brewers": "MIL",
    "Minnesota Twins": "MIN",
    "New York Mets": "NYM",
    "New York Yankees": "NYY",
    "Oakland Athletics": "OAK",
    "Philadelphia Phillies": "PHI",
    "Pittsburgh Pirates": "PIT",
    "San Diego Padres": "SD",
    "San Francisco Giants": "SF",
    "Seattle Mariners": "SEA",
    "St. Louis Cardinals": "STL",
    "Tampa Bay Rays": "TB",
    "Texas Rangers": "TEX",
    "Toronto Blue Jays": "TOR",
    "Washington Nationals": "WSH"
}

def rate_confidence_for_game(game: dict, sharp_data: dict) -> dict | None:
    away_full = game.get("away_team")
    home_full = game.get("home_team")
    odds_home = game.get("home_odds")
    odds_away = game.get("away_odds")

    if not all([away_full, home_full, isinstance(odds_home, (int, float)), isinstance(odds_away, (int, float))]):
        print(f"[⚠️ Skipped] Incomplete game data — {away_full} vs {home_full}")
        return None

    away = TEAM_ABBREVIATIONS.get(away_full)
    home = TEAM_ABBREVIATIONS.get(home_full)
    if not away or not home:
        print(f"[⚠️ Skipped] No abbreviation for {away_full} or {home_full}")
        return None

    matchup_key = (away, home)
    game_str = f"{away_full} vs {home_full}"

    sharp = sharp_data.get(matchup_key)
    if not sharp or "bet_pct" not in sharp or "money_pct" not in sharp:
        print(f"[⚠️ Sharp Missing] {game_str}")
        return None

    bet_pct = sharp["bet_pct"]
    money_pct = sharp["money_pct"]
    sharp_delta = money_pct - bet_pct

    if sharp_delta < 30:
        print(f"[⛔ Skipped] {game_str} — Sharp delta {sharp_delta}% too low")
        return None

    confidence = 5.0 + min(max(sharp_delta / 3, 0), 10) * 0.5
    if confidence < 7.5:
        print(f"[⛔ Skipped] {game_str} — Confidence {round(confidence,1)} too low")
        return None

    pick_side = home_full if odds_home > odds_away else away_full
    pick_type = "ML"
    odds = odds_home if pick_side == home_full else odds_away
    stake = round((confidence - 5.0) / 5 * 2, 2)

    return {
        "game": game_str,
        "pick": f"{pick_side} {pick_type}",
        "confidence": round(confidence, 1),
        "sharp_delta": sharp_delta,
        "odds": odds,
        "stake": stake,
        "status": "Not Started",
        "why": f"{pick_side} has edge with sharp delta {sharp_delta}% and model score {round(confidence,1)}"
    }
