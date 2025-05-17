from flask import Flask, render_template_string, request
from mlb.engine import get_today_mlb_picks

app = Flask(__name__)

HTML = """
<!doctype html>
<title>Xclusive Sports Picks</title>
<h1>🧢 Today's MLB Picks</h1>
<ul>
  {% for pick in picks %}
    <li>
      <strong>{{ pick['matchup'] }}</strong><br>
      Confidence: {{ pick['confidence'] }}<br>
      Sharp Delta: {{ pick['sharp_delta'] }}<br>
      Odds: {{ pick['odds'] }}<br>
      Stake: {{ pick['stake'] }}<br>
      Why: {{ pick['why'] }}<br>
    </li>
  {% endfor %}
</ul>
"""

@app.route("/")
def index():
    try:
        picks = get_today_mlb_picks()
    except Exception as e:
        picks = []
        print("Error:", e)
    return render_template_string(HTML, picks=picks)
