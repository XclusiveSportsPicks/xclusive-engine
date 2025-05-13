# app.py

from flask import Flask, jsonify, render_template
from flask_caching import Cache
import requests
import datetime

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# --- Core Config ---
SHARP_THRESHOLD = 30  # Money% must exceed Bet% by 30%
CONFIDENCE_THRESHOLD = 7.5
AUTO_REFRESH_MINUTES = 10

# --- Mock External API ---
def fetch_external_data():
    # This should pull from ESPN/Flashscore/sportsbooks
    # Replace with actual API consumption
    return [
        {
            'game': 'Celtics vs Heat',
            'bet': 'Celtics -6.5',
            'odds': -110,
            'confidence': 8.9,
            'bet_pct': 42,
            'money_pct': 76,
            'status': 'In Progress',
            'final_result': None
        },
        {
            'game': 'Yankees vs Red Sox',
            'bet': 'Yankees ML',
            'odds': +105,
            'confidence': 7.6,
            'bet_pct': 33,
            'money_pct': 66,
            'status': 'Scheduled',
            'final_result': None
        }
    ]

# --- Sharp % Calculation ---
def calculate_sharp_percent(bet_pct, money_pct):
    return round(money_pct - bet_pct)

# --- Picks Builder ---
def fetch_picks():
    try:
        raw_data = fetch_external_data()
        picks = []
        for item in raw_data:
            try:
                sharp_delta = calculate_sharp_percent(item['bet_pct'], item['money_pct'])
                if sharp_delta >= SHARP_THRESHOLD and item['confidence'] >= CONFIDENCE_THRESHOLD:
                    picks.append({
                        'game': item['game'],
                        'pick': item['bet'],
                        'odds': item['odds'],
                        'confidence': item['confidence'],
                        'sharp_percent': sharp_delta,
                        'status': item['status'],
                        'result': item.get('final_result', '')
                    })
            except Exception as inner_err:
                print(f"[Pick Parse Error] {inner_err}")
    except Exception as err:
        print(f"[Fetch Error] {err}")
        return []
    return picks

# --- Homepage Route ---
@app.route('/')
def home():
    picks = fetch_picks()
    return render_template('index.html', picks=picks)

# --- Auto-Updated Picks API ---
@cache.cached(timeout=AUTO_REFRESH_MINUTES * 60, key_prefix='auto_picks')
@app.route('/api/auto-picks')
def api_auto_picks():
    picks = fetch_picks()
    return jsonify({'picks': picks, 'updated': datetime.datetime.utcnow().isoformat()})

# --- League Filtered Picks Endpoint (Placeholder for future logic) ---
@app.route('/api/leagues')
def api_leagues():
    # Stub response; league filtering can be added later
    return jsonify({'available_leagues': ['NBA', 'MLB', 'NHL']})

# --- Run (Local Testing Only) ---
if __name__ == '__main__':
    app.run(debug=True)
