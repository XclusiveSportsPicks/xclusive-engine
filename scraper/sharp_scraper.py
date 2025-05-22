
from bs4 import BeautifulSoup
import requests

TEAM_NAME_MAP = {
    "NY Yankees": "New York Yankees",
    "LA Dodgers": "Los Angeles Dodgers",
    # Add more mappings as needed
}

def normalize(name):
    return TEAM_NAME_MAP.get(name, name)

def scrape_scoresandodds():
    url = "https://www.scoresandodds.com/mlb/consensus-picks"
    res = requests.get(url, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")
    data = {}

    rows = soup.select("table tbody tr")
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 5:
            team = normalize(cells[0].get_text(strip=True))
            bets = int(cells[2].get_text(strip=True).replace("%", ""))
            money = int(cells[3].get_text(strip=True).replace("%", ""))
            data[team] = {"bet_pct": bets, "money_pct": money}

    return data

def scrape_actionnetwork():
    url = "https://www.actionnetwork.com/mlb/public-betting"
    res = requests.get(url, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")
    data = {}

    rows = soup.select("table tr")
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 4:
            team = normalize(cells[0].get_text(strip=True))
            bets = int(cells[2].get_text(strip=True).replace("%", ""))
            money = int(cells[3].get_text(strip=True).replace("%", ""))
            data[team] = {"bet_pct": bets, "money_pct": money}

    return data

def get_sharp_data():
    try:
        return scrape_scoresandodds()
    except:
        return scrape_actionnetwork()
