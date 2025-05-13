from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
import requests
import os

app = Flask(__name__)

API_KEY = "1256c747dab65e1c3cd504f9a3f4802b"
ODDS_API_URL = "https://api.the-odds-api.com/v4/sports/{sport}/odds"
ESPN_SCORES = {
    "MLB": "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard",
    "NBA": "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard",
    "NFL": "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard",
    "NHL": "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard",
    "NCAAB": "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard"
}
WEATHER_API_KEY = "demo"
WEATHER_ENDPOINT = "https://api.weatherapi.com/v1/current.json"

CACHE = {
    "timestamp": None,
    "picks": []
}

from datetime import datetime

def get_active_leagues():
    return {
        "MLB": "baseball_mlb",
        "NBA": "basketball_nba",
        "NHL": "icehockey_nhl",
        "SOCCER": "soccer_epl"
        # NFL, NCAAF, and other off-season leagues are temporarily disabled
    }


EMOJIS = {
    "MLB": "⚾️", "NBA": "🏀", "NFL": "🏈",
    "NHL": "🏒", "SOCCER": "⚽️", "NCAAB": "🎓"
}

def get_espn_game_status(league, team1, team2):
    url = ESPN_SCORES.get(league)
    if not url:
        return "Scheduled"
    try:
        res = requests.get(url)
        data = res.json()
        for event in data.get("events", []):
            names = [c.get("team", {}).get("displayName", "") for c in event.get("competitions", [{}])[0].get("competitors", [])]
            if team1 in names or team2 in names:
                status = event.get("status", {}).get("type", {}).get("description", "Scheduled")
                return status
    except:
        pass
    return "Scheduled"

def get_weather_risk(team):
    try:
        params = {"key": WEATHER_API_KEY, "q": team}
        r = requests.get(WEATHER_ENDPOINT, params=params)
        if r.status_code == 200:
            data = r.json()
            condition = data["current"]["condition"]["text"]
            precip = data["current"].get("precip_in", 0)
            return condition.lower(), float(precip) >= 0.2
    except:
        pass
    return "clear", False

def fetch_picks():
    picks = []
    total_checked = 0
    skipped = 0
    for league, sport_key in get_active_leagues().items():
        try:
            response = requests.get(
                ODDS_API_URL.format(sport=sport_key),
                params={"apiKey": API_KEY, "regions": "us", "markets": "h2h,spreads", "oddsFormat": "american"}
            )
            if response.status_code != 200:
                print(f"[ERROR] Failed to fetch {league} data: {response.status_code}")
                continue

            games = response.json()
            print(f"[INFO] {league} - Games found: {len(games)}")

            for game in games:
                total_checked += 1
try:
    teams = game.get("teams") or [game.get("home_team"), game.get("away_team")]

    if len(teams) < 2:
        skipped += 1
        print(f"[SKIP] {league} - Missing teams")
        continue


                    bookmakers = game.get("bookmakers", [])
                    if not bookmakers or not bookmakers[0].get("markets"):
                        skipped += 1
                        print(f"[SKIP] {league} - No markets")
                        continue

                    outcomes = bookmakers[0]["markets"][0].get("outcomes", [])
                    if not outcomes or len(outcomes) < 1:
                        skipped += 1
                        print(f"[SKIP] {league} - No outcomes")
                        continue

                    team_1, team_2 = teams
                    chosen = outcomes[0]["name"]
                    odds = outcomes[0]["price"]
                    open_odds = outcomes[0].get("point", odds)

                    line_movement = odds - open_odds
                    sharp_tag = "Sharp Side" if abs(line_movement) >= 10 and line_movement < 0 else (
                                "Public Fade" if abs(line_movement) >= 10 else "None")
                    estimated_sharp_pct = min(95, 60 + abs(line_movement))

                    status = get_espn_game_status(league, team_1, team_2)
                    condition, weather_alert = get_weather_risk(team_1 if league == "MLB" else team_2)

                    confidence_score = 7.0
                    if sharp_tag == "Sharp Side": confidence_score += 1.0
                    elif sharp_tag == "Public Fade": confidence_score += 0.5
                    if abs(line_movement) >= 15: confidence_score += 0.5
                    if weather_alert: confidence_score -= 0.5
                    confidence_score = round(confidence_score, 1)

                    if confidence_score >= 9.0:
                        confidence = "Elite 🔒 Max Confidence"
                    elif confidence_score >= 8.0:
                        confidence = "High"
                    elif confidence_score >= 7.0:
                        confidence = "Medium"
                    else:
                        confidence = "Low"

                    picks.append({
                        "league": league,
                        "emoji": EMOJIS.get(league, ""),
                        "game": f"{team_1} vs {team_2}",
                        "pick": chosen,
                        "odds": odds,
                        "sharp": f"{estimated_sharp_pct}%",
                        "confidence": confidence,
                        "confidence_score": confidence_score,
                        "status": status,
                        "weather_alert": weather_alert,
                        "weather": condition,
                        "line_movement": line_movement,
                        "sharp_tag": sharp_tag
                    })
                except Exception as e:
                    skipped += 1
                    print(f"[SKIP] {league} - Error processing game: {e}")
        except Exception as e:
            print(f"[ERROR] Fetch error for {league}: {e}")

    print(f"[SUMMARY] Total checked: {total_checked}, Skipped: {skipped}, Final picks: {len(picks)}")

    picks = sorted(picks, key=lambda x: x["confidence_score"], reverse=True)
    if picks and "Elite" not in picks[0]["confidence"]:
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
    picks = fetch_picks()
    CACHE["timestamp"] = now
    CACHE["picks"] = picks
    return jsonify(picks)

@app.route("/api/leagues")
def get_leagues():
    return jsonify(list(LEAGUE_MAP.keys()))

if __name__ == "__main__":
    app.run(debug=True)
