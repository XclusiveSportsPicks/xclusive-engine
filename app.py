# Xclusive Backend Engine (MVP)
# Flask app that applies sharp logic and serves picks via API

from flask import Flask, jsonify
import datetime

app = Flask(__name__)

# --- Config: thresholds ---
CONFIDENCE_THRESHOLDS = {
    'MLB': 8.8,
    'NBA': 8.5,
    'Soccer': 8.3
}

SHARP_DELTA_REQUIREMENT = {
    'MLB': 35,
    'NBA': 25,
    'Soccer': 25
}

# --- Sample Stub Data (Replace with API ingestion later) ---
RAW_GAMES = [
    {
        'sport': 'MLB',
        'game': 'Yankees vs Red Sox',
        'pick': 'Yankees ML',
        'odds': -120,
        'confidence': 9.1,
        'bet_pct': 40,
        'money_pct': 78,
        'line_open': -110,
        'line_current': -120,
        'injury_flag': False,
        'pitcher_change': False,
        'model_prediction': 'Yankees win 5-3'
    },
    {
        'sport': 'NBA',
        'game': 'Warriors vs Lakers',
        'pick': 'Over 228.5',
        'odds': -110,
        'confidence': 8.2,
        'bet_pct': 67,
        'money_pct': 69,
        'line_open': 227,
        'line_current': 228.5,
        'injury_flag': True,
        'pitcher_change': False,
        'model_prediction': 'Total = 230'
    }
]

# --- Pick Filtering Logic ---
def is_valid_pick(g):
    confidence_ok = g['confidence'] >= CONFIDENCE_THRESHOLDS[g['sport']]
    sharp_delta = g['money_pct'] - g['bet_pct']
    sharp_ok = sharp_delta >= SHARP_DELTA_REQUIREMENT[g['sport']]
    line_ok = g['line_current'] >= g['line_open']  # No reverse move
    injury_ok = not g['injury_flag'] and not g['pitcher_change']
    return confidence_ok and sharp_ok and line_ok and injury_ok

# --- API Route ---
@app.route('/picks', methods=['GET'])
def get_picks():
    picks = []
    for g in RAW_GAMES:
        if is_valid_pick(g):
            picks.append({
                'Game & Bet': f"{g['game']} — {g['pick']}",
                'Confidence Score': g['confidence'],
                'Sharp %': f"{g['bet_pct']}% bets / {g['money_pct']}% money",
                'Why I Like It': 'Sharp delta + model match + no injury flags.',
                'Model Prediction': g['model_prediction'],
                'Xs Absolute Best Bet': '✅' if g['confidence'] >= 9 else ''
            })

    return jsonify({
        'date': datetime.date.today().isoformat(),
        'picks': picks
    })

# --- Main App ---
if __name__ == '__main__':
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)

