# backend/filters.py
import os, requests, logging
from dotenv import load_dotenv

load_dotenv()
ESPN_SUMMARY_URL = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/summary"

def is_game_final(matchup: str) -> bool:
    home, _, away = matchup.partition(" vs ")
    try:
        res = requests.get(ESPN_SUMMARY_URL)
        res.raise_for_status()
        for event in res.json().get("events", []):
            teams = {c["team"]["name"] for c in event["competitions"][0]["competitors"]}
            if {home, away}.issubset(teams):
                status = event["status"]["type"]["detail"].lower()
                return status.startswith("final")
    except Exception as e:
        logging.warning(f"[is_game_final] {matchup}: {e}")
    return False

def line_moved_in_your_direction(open_odds: float, current_odds: float, pick_side: str) -> bool:
    side = pick_side.lower()
    # Moneyline favorite vs underdog
    if side in ("home", "favorite"):
        return current_odds <= open_odds
    if side in ("away", "underdog"):
        return current_odds >= open_odds
    # Totals
    if side == "over":
        return current_odds <= open_odds
    if side == "under":
        return current_odds >= open_odds
    # Spread same as moneyline logic
    if side in ("home", "away"):
        return current_odds <= open_odds
    return True
