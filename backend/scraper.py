# backend/scraper.py

import os, logging
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright
from apscheduler.schedulers.background import BackgroundScheduler

from models import db, Pick
from filters import is_game_final, line_moved_in_your_direction

logging.basicConfig(level=logging.INFO)
ODDS_API_KEY = os.getenv("ODDS_API_KEY")
if not ODDS_API_KEY:
    raise RuntimeError("ODDS_API_KEY not set")

def scrape_consensus_sharp_pct():
    url = "https://www.scoresandodds.com/mlb/consensus-picks"
    out=[]
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        rows = page.locator("table tbody tr")
        for i in range(rows.count()):
            row = rows.nth(i)
            m   = row.locator("td:nth-child(1)").inner_text().strip()
            sp  = float(row.locator("td:nth-child(2)").inner_text().rstrip("%"))
            bp  = float(row.locator("td:nth-child(3)").inner_text().rstrip("%"))
            out.append({"matchup": m, "sharp_pct": sp, "bet_pct": bp})
        browser.close()
    logging.info(f"Consensus: {len(out)} rows")
    return out

def scrape_public_betting():
    url = "https://www.actionnetwork.com/mlb/public-betting"
    res = requests.get(url); soup = BeautifulSoup(res.text, "html.parser")
    out=[]
    for r in soup.select("table.public-betting tbody tr"):
        m = r.select_one(".matchup").get_text(strip=True)
        s = float(r.select_one(".sharp-pct").get_text(strip=True).rstrip("%"))
        b = float(r.select_one(".bet-pct").get_text(strip=True).rstrip("%"))
        out.append({"matchup":m, "sharp_pct":s, "bet_pct":b})
    return out

def scrape_line_movement():
    url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds?apiKey={ODDS_API_KEY}&regions=us&markets=h2h"
    data = requests.get(url).json(); out=[]
    for e in data:
        m = f"{e['home_team']} vs {e['away_team']}"
        o = e['bookmakers'][0]['markets'][0]['outcomes'][0]
        open_odds = o.get('price_open', o['price'])
        cur_odds  = o['price']
        mov = abs(cur_odds - open_odds)
        out.append({
          "matchup": m,
          "open_odds": open_odds,
          "current_odds": cur_odds,
          "line_movement_score": mov
        })
    return out

def scrape_moneyline_odds():
    url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds?apiKey={ODDS_API_KEY}&regions=us&markets=h2h&oddsFormat=american"
    data = requests.get(url).json(); out=[]
    for e in data:
        m = f"{e['home_team']} vs {e['away_team']}"
        for o in e['bookmakers'][0]['markets'][0]['outcomes']:
            out.append({
                "matchup": m, "type":"moneyline",
                "side":o['name'], "odds_american":o['price'],
                "open_odds": o.get('price_open', o['price']),
                "current_odds": o['price']
            })
    return out

def scrape_totals_odds():
    url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds?apiKey={ODDS_API_KEY}&regions=us&markets=totals&oddsFormat=american"
    data = requests.get(url).json(); out=[]
    for e in data:
        m = f"{e['home_team']} vs {e['away_team']}"
        for o in e['bookmakers'][0]['markets'][0]['outcomes']:
            out.append({
                "matchup": m, "type":"total", "side":o['name'].lower(),
                "total_line":o['point'], "odds_american":o['price'],
                "open_odds": o.get('point_open', o['point']),
                "current_odds": o['point']
            })
    return out

def scrape_spreads_odds():
    url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds?apiKey={ODDS_API_KEY}&regions=us&markets=spreads&oddsFormat=american"
    data = requests.get(url).json(); out=[]
    for e in data:
        m = f"{e['home_team']} vs {e['away_team']}"
        for o in e['bookmakers'][0]['markets'][0]['outcomes']:
            out.append({
                "matchup": m, "type":"spread", "side":o['name'],
                "spread_line":o['point'], "odds_american":o['price'],
                "open_odds": o.get('point_open', o['point']),
                "current_odds": o['point']
            })
    return out

def scrape_pitcher_props():
    return []  # implement as needed

def scrape_hitter_stats():
    return []  # implement as needed

def run_scraper():
    sources = [
      scrape_consensus_sharp_pct(),
      scrape_public_betting(),
      scrape_line_movement(),
      scrape_moneyline_odds(),
      scrape_totals_odds(),
      scrape_spreads_odds(),
      scrape_pitcher_props(),
      scrape_hitter_stats()
    ]
    merged = {}
    for src in sources:
        for p in src:
            key = (p["matchup"], p.get("type","pitcher"), p.get("side"))
            merged.setdefault(key, {}).update(p)

    with db.session.begin():
        count=0
        for (matchup, ptype, side), v in merged.items():
            if not is_game_final(matchup):
                continue
            if "open_odds" in v and "current_odds" in v:
                if not line_moved_in_your_direction(v["open_odds"], v["current_odds"], v.get("side","")):
                    continue
            if ptype=="pitcher" and v.get("pitcher_edge",0)<2.0:
                continue
            if ptype=="hitter" and not (v.get("iso",0)>=0.2 and v.get("sharp_pct",0)>=v.get("bet_pct",0)+30):
                continue

            pick = db.session.query(Pick).filter_by(
                matchup=matchup, type=ptype, side=side
            ).first() or Pick(matchup=matchup, type=ptype, side=side)

            for f in ["sharp_pct","bet_pct","iso","pitcher_edge",
                      "line_movement_score","open_odds","current_odds",
                      "total_line","spread_line","odds_american","model_edge"]:
                if f in v:
                    setattr(pick, f, v[f])

            if ptype in ("pitcher","hitter"):
                cs = ((pick.model_edge/3.0)*0.5 +
                      (pick.sharp_pct/100.0)*0.3 +
                      pick.line_movement_score*0.2)*10
                pick.confidence_score = round(cs,1)
                wp = ((cs/10.0)*0.6 +
                      (pick.sharp_pct/100.0)*0.3 +
                      pick.line_movement_score*0.1)*100
                pick.win_probability = round(wp,1)

            if ptype in ("moneyline","spread","total"):
                pick.summary = f"{v.get('side','')} @ {v.get('odds_american')}"

            db.session.merge(pick)
            count+=1

    logging.info(f"Saved {count} picks")
    return {"scraped_at": datetime.utcnow().isoformat(), "count": count}

def schedule_jobs(app):
    sched = BackgroundScheduler(timezone="US/Eastern")
    sched.add_job(run_scraper, "cron", hour="10,15,18", minute=0)
    sched.start()
    return sched
