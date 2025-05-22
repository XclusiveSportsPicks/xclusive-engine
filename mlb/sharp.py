from mlb.sharp_scraper import scrape_scoresandodds_sharp_data

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

def get_sharp_data():
    try:
        raw_data = scrape_scoresandodds_sharp_data()
        if not isinstance(raw_data, dict):
            print("[❌ Sharp Fetch Error] Returned non-dict object")
            return {}

        mapped_data = {}
        for (away_full, home_full) in raw_data:
            away = TEAM_ABBREVIATIONS.get(away_full)
            home = TEAM_ABBREVIATIONS.get(home_full)
            if not away or not home:
                print(f"[⚠️ Skip Mapping] Unknown teams: {away_full}, {home_full}")
                continue

            key = (away, home)
            mapped_data[key] = raw_data[(away_full, home_full)]

        print(f"[✅ Sharp Mapper] Mapped {len(mapped_data)} matchups")
        return mapped_data

    except Exception as e:
        print(f"[❌ Sharp Data Error] {str(e)}")
        return {}
