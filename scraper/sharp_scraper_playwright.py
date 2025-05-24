
import asyncio
from playwright.async_api import async_playwright
import re

TEAM_NAME_MAP = {
    "BAL": "Baltimore Orioles", "BOS": "Boston Red Sox", "NYY": "New York Yankees", "ATL": "Atlanta Braves",
    "PHI": "Philadelphia Phillies", "LAD": "Los Angeles Dodgers", "SD": "San Diego Padres", "OAK": "Oakland Athletics",
    "TEX": "Texas Rangers", "MIL": "Milwaukee Brewers", "COL": "Colorado Rockies", "TOR": "Toronto Blue Jays",
    "PIT": "Pittsburgh Pirates", "LAA": "Los Angeles Angels", "CHC": "Chicago Cubs", "CLE": "Cleveland Guardians",
    "KC": "Kansas City Royals", "MIA": "Miami Marlins", "SF": "San Francisco Giants", "CWS": "Chicago White Sox",
    "SEA": "Seattle Mariners", "ARI": "Arizona Diamondbacks", "NYM": "New York Mets", "TB": "Tampa Bay Rays",
    "STL": "St. Louis Cardinals", "HOU": "Houston Astros", "MIN": "Minnesota Twins", "WSH": "Washington Nationals",
    "DET": "Detroit Tigers"
}

def normalize(name):
    return TEAM_NAME_MAP.get(name.strip().upper(), name.strip())

async def scrape_sao_live():
    print("📊 Starting full DOM scrape with logging...")
    sharp_data = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = await browser.new_page()
        await page.goto("https://www.scoresandodds.com/mlb/consensus-picks", timeout=90000)
        await page.wait_for_timeout(8000)

        html = await page.content()
        print(f"📄 First 500 chars of page HTML:\n{html[:500]}")

        cards = await page.query_selector_all("div.event-header")
        print(f"📦 Found {len(cards)} matchups on SAO")

        for card in cards:
            try:
                teams = await card.query_selector_all("span.team-name span")
                if len(teams) != 2:
                    continue
                team1 = normalize(await teams[0].inner_text())
                team2 = normalize(await teams[1].inner_text())
                print(f"🟢 Matchup: {team1} vs {team2}")

                parent = await card.evaluate_handle("node => node.parentElement")
                all_divs = await parent.query_selector_all("div")

                bet_pcts = money_pcts = None
                for div in all_divs:
                    raw_text = raw_text
                    print(f"🧩 DIV TEXT: {raw_text}")
                    text = raw_text
                    if "Bets" in text and "%" in text:
                        print(f"📊 Bets block: {text}")
                        nums = list(map(int, re.findall(r"(\d+)%", text)))[:2]
                        if len(nums) == 2:
                            bet_pcts = nums
                    if "Money" in text and "%" in text:
                        print(f"💰 Money block: {text}")
                        nums = list(map(int, re.findall(r"(\d+)%", text)))[:2]
                        if len(nums) == 2:
                            money_pcts = nums

                if bet_pcts and money_pcts:
                    sharp_data[team1] = {
                        "opponent": team2,
                        "bet_pct": bet_pcts[0],
                        "money_pct": money_pcts[0],
                        "source": "ScoresAndOdds"
                    }
                    sharp_data[team2] = {
                        "opponent": team1,
                        "bet_pct": bet_pcts[1],
                        "money_pct": money_pcts[1],
                        "source": "ScoresAndOdds"
                    }

            except Exception as e:
                print(f"[!] Scrape error: {e}")
                continue

        await browser.close()
        print(f"✅ Final scraped teams: {list(sharp_data.keys())}")
        return sharp_data

if __name__ == "__main__":
    asyncio.run(scrape_sao_live())
