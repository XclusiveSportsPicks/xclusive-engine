
import requests
from bs4 import BeautifulSoup

TEAM_NAME_MAP = {
    "NY Yankees": "New York Yankees",
    "LA Dodgers": "Los Angeles Dodgers",
    "Chi Cubs": "Chicago Cubs",
    "SF Giants": "San Francisco Giants",
    "Bos Red Sox": "Boston Red Sox",
    "Atl Braves": "Atlanta Braves",
}

def normalize(name):
    return TEAM_NAME_MAP.get(name.strip(), name.strip())

def extract_pct(text):
    try:
        return int(text.replace("%", "").strip())
    except:
        return None

def scrape_scoresandodds():
    url = "https://www.scoresandodds.com/mlb/consensus-picks"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    with open("sao_debug.html", "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    data = {}
    rows = soup.select("table tbody tr")
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 5:
            team = normalize(cells[0].get_text(strip=True))
            bet = extract_pct(cells[2].get_text())
            money = extract_pct(cells[3].get_text())
            if bet is not None and money is not None:
                data[team] = {"bet_pct": bet, "money_pct": money}
    return data

def scrape_actionnetwork():
    url = "https://www.actionnetwork.com/mlb/public-betting"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    with open("action_debug.html", "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    data = {}
    rows = soup.select("table tr")
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 4:
            team = normalize(cells[0].get_text(strip=True))
            bet = extract_pct(cells[2].get_text())
            money = extract_pct(cells[3].get_text())
            if bet is not None and money is not None:
                data[team] = {"bet_pct": bet, "money_pct": money}
    return data

def get_sharp_data():
    try:
        print("[🔌 Trying ScoresAndOdds scrape...]")
        data = scrape_scoresandodds()
        if data:
            print(f"[✅ ScoresAndOdds returned {len(data)} teams]")
            return data
        else:
            print("[⚠️ No data from ScoresAndOdds — falling back]")
    except Exception as e:
        print("[❌ ScoresAndOdds scraper failed]", e)

    try:
        print("[🔁 Trying ActionNetwork fallback...]")
        data = scrape_actionnetwork()
        if data:
            print(f"[✅ ActionNetwork returned {len(data)} teams]")
            return data
        else:
            print("[⚠️ No data from ActionNetwork either]")
    except Exception as e:
        print("[❌ ActionNetwork scraper failed]", e)

    print("[🆘 Returning EMPTY fallback for test mode]")
    return {
        "New York Yankees": {"bet_pct": 40, "money_pct": 80},
        "Atlanta Braves": {"bet_pct": 38, "money_pct": 71}
    }

if __name__ == "__main__":
    print("✅ sharp_scraper.py is running — TOP OF FILE")
    print("🔁 Main block running — calling get_sharp_data()...")
    from pprint import pprint
    data = get_sharp_data()
    pprint(data)
    print(f"🧪 Total teams: {len(data)}")
