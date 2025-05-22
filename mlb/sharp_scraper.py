import requests
from bs4 import BeautifulSoup

def scrape_scoresandodds_sharp_data():
    url = "https://www.scoresandodds.com/mlb/consensus-picks"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    sharp_data = {}
    matchups = soup.find_all("span", class_="trend-graph-chart")

    print(f"[🔍 DEBUG] Found {len(matchups)} matchups")

    for block in matchups:
        teams = block.find("span", class_="trend-graph-sides")
        if not teams:
            continue

        team_tags = teams.find_all("strong")
        if len(team_tags) != 2:
            continue

        team_a = team_tags[0].text.strip()
        team_b = team_tags[1].text.strip()
        matchup = f"{team_a} vs {team_b}"

        # Grab all trend-graph-percentage spans (expecting Bets first, Money second)
        percentages = block.find_all("span", class_="trend-graph-percentage")
        if len(percentages) < 2:
            continue

        def extract_pct_data(block):
            spans = block.find_all("span", class_=["percentage-a", "percentage-b"])
            try:
                values = [int(span.text.strip().replace('%', '')) for span in spans]
                return max(values) if values else None
            except:
                return None

        bet_pct = extract_pct_data(percentages[0])
        money_pct = extract_pct_data(percentages[1])

        if bet_pct is None or money_pct is None:
            continue

        sharp_data[(team_a, team_b)] = {
            "bet_pct": bet_pct,
            "money_pct": money_pct
        }

    print(f"[✅ Sharp Scraper] Pulled {len(sharp_data)} matchups")

    # 📊 Bonus Debug Tip — Log matched matchups with percentages
    for matchup, values in sharp_data.items():
        print(f"[📊 SHARP] {matchup}: Bets {values['bet_pct']}%, Money {values['money_pct']}%")

    return sharp_data
