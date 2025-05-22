# utils/team_name_map.py

TEAM_NAME_MAP = {
    "NY Yankees": "New York Yankees",
    "LA Dodgers": "Los Angeles Dodgers",
    "Chi Cubs": "Chicago Cubs",
    "SF Giants": "San Francisco Giants",
    "Bos Red Sox": "Boston Red Sox",
    "Atl Braves": "Atlanta Braves",
    # ✅ Add more mappings as needed
}

def normalize_team_name(raw_name):
    return TEAM_NAME_MAP.get(raw_name.strip(), raw_name.strip())

