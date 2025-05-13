from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

ODDS_API_KEY = "1256c747dab65e1c3cd504f9a3f4802b"
SPORTS = {
    "NBA": {"odds_key": "basketball_nba", "espn": "basketball/nba", "emoji": "🏀"},
    "MLB": {"odds_key": "baseball_mlb", "espn": "baseball/mlb", "emoji": "⚾️"},
    "NFL": {"odds_key": "americanfootball_nfl", "espn": "football/nfl", "emoji": "🏈"},
    "NHL": {"odds_key": "icehockey_nhl", "espn": "hockey/nhl", "emoji": "🏒"},
    "SOCCER": {"odds_key": "soccer_epl", "espn": "soccer/eng.1", "emoji": "⚽️"},
    "NCAAB": {"odds_key": "basketball_ncaab", "espn": "basketball/mens-college-basketball", "emoji": "🎓"}
}
BOOKMAKER = "draftkings"
CACHE = {"timestamp": None, "picks": [], "status": {}}


def kelly_fraction(prob, odds):
    b = abs((odds / 100) if odds > 0 else (100 / abs(odds))) - 1
    f = (prob * (b + 1) - 1) / b if b > 0 else 0
    return max(0, min(f * 0.5, 1))


def fetch_espn_status():
    status_map = {}
    for league, meta in SPORTS.items():
        url = f"https://site.api.espn.com/apis/site/v2/sports/{meta['espn']}/scoreboard"
        try:
            r = requests.get(url, timeout=5)
            events = r.json().get("events", [])
            for game in events:
                name = game.get("shortName", "")
                status = game.get("status", {}).get("type", {}).get("name", "")
                status_map[name] = "Confirmed Final" if "FINAL" in status else "In Progress"
        except Exception as e:
            print(f"[ESPN ERROR] {league} failed: {e}")
    return status_map


def fetch_all_picks():
    picks = []
    for league, meta in SPORTS.items():
        url = f"https://api.the-odds-api.com/v4/sports/{meta['odds_key']}/odds"
        try:
            r = requests.get(url, params={
                "apiKey": ODDS_API_KEY,
                "regions": "us",
                "markets": "h2h",
                "bookmakers": BOOKMAKER
            })
            if r.status_code != 200:
                print(f"[ODDSAPI ERROR] {league}: {r.status_code} - {r.text}")
                continue

            games = r.json()
            print(f"[INFO] {league} - Games found: {len(games)}")
            for game in games:
                home = game.get("home_team", "")
                away = game.get("away_team", "")
                matchup = f"{home} vs {away}"

                bookmakers = game.get("bookmakers", [])
                if not bookmakers:
                    print(f"[SKIP] {matchup} - no bookmakers")
                    continue

                markets = bookmakers[0].get("markets", [])
                if not markets:
                    print(f"[SKIP] {matchup} - no markets")
                    continue

                outcomes = markets[0].get("outcomes", [])
                if len(outcomes) < 2:
                    print(f"[SKIP] {matchup} - incomplete outcomes")
                    continue

                for outcome in outcomes:
                    team = outcome.get("name")
                    odds = outcome.get("price")
                    bet_pct = outcome.get("bet_percentage", 0)
                    money_pct = outcome.get("money_percentage", 0)
                    sharp_delta = money_pct - bet_pct
                    if sharp_delta < 30:
                        continue
                    score = (money_pct + sharp_delta) / 2
                    tier = "Elite 🔒 Max Confidence" if score >= 88 else "High" if score >= 75 else "Medium" if score >= 66 else "Low"
                    stake_pct = kelly_fraction(money_pct / 100, odds)
                    picks.append({
                        "league": league,
                        "emoji": meta["emoji"],
                        "game": matchup,
                        "pick": team,
                        "odds": odds,
                        "sharp": f"{money_pct}%",
                        "confidence": tier,
                        "stake": round(stake_pct * 100),
                        "sharp_delta": sharp_delta
                    })
        except Exception as e:
            print(f"[ODDSAPI ERROR] {league} exception: {e}")
            continue

    print(f"[DEBUG] {len(picks)} sharp-qualified picks generated.")

    picks = sorted(picks, key=lambda x: x["sharp_delta"], reverse=True)
    if picks:
        picks[0]["confidence"] += " 🔥 X's Absolute Best Bet"
    return picks


@app.route("/")
def index():
    return render_template("index.html", last_updated=datetime.now().strftime("%Y-%m-%d %H:%M"))


@app.route("/api/auto-picks")
def auto_picks():
    now = datetime.now()
    if CACHE["timestamp"] and now - CACHE["timestamp"] < timedelta(minutes=10):
        return jsonify(CACHE["picks"])
    CACHE["picks"] = fetch_all_picks()
    CACHE["status"] = fetch_espn_status()
    CACHE["timestamp"] = now
    return jsonify(CACHE["picks"])


@app.route("/api/game-status")
def game_status():
    return jsonify(CACHE["status"] if CACHE["status"] else fetch_espn_status())


if __name__ == "__main__":
    app.run(debug=True)
