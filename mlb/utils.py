def extract_abbr(team_name):
    abbr_map = {
        "Yankees": "nyy", "Mets": "nym", "Red Sox": "bos", "Blue Jays": "tor",
        "Rays": "tb", "Orioles": "bal", "White Sox": "cws", "Guardians": "cle",
        "Tigers": "det", "Royals": "kc", "Twins": "min", "Astros": "hou",
        "Angels": "laa", "Mariners": "sea", "Rangers": "tex", "Athletics": "oak",
        "Braves": "atl", "Marlins": "mia", "Nationals": "was", "Phillies": "phi",
        "Cubs": "chc", "Reds": "cin", "Brewers": "mil", "Pirates": "pit",
        "Cardinals": "stl", "Diamondbacks": "ari", "Rockies": "col", "Dodgers": "lad",
        "Giants": "sf", "Padres": "sd"
    }
    return abbr_map.get(team_name.strip(), "mlb")

def normalize_matchup(matchup):
    # "Boston Red Sox vs New York Mets" → "bos@nym"
    try:
        team1, team2 = matchup.split(" vs ")
        return f"{extract_abbr(team1)}@{extract_abbr(team2)}"
    except Exception:
        return "mlb@mlb"

def match_sharp_to_pick(pick_matchup, sharp_data):
    normalized_pick = normalize_matchup(pick_matchup)
    for sharp_matchup in sharp_data:
        normalized_sharp = normalize_matchup(sharp_matchup)
        if normalized_pick == normalized_sharp:
            return sharp_data[sharp_matchup]
    return {"money_pct": 0, "bet_pct": 0}
