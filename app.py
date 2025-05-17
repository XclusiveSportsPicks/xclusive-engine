# app.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "mlb"))
from dotenv import load_dotenv
import os
from flask import Flask, render_template, request
from datetime import datetime
from engine import get_today_mlb_picks

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", "xclusive-dev-key")

@app.route("/")
def index():
    league = request.args.get("league", "MLB")

    if league == "MLB":
        picks = get_today_mlb_picks()
    else:
        picks = []  # placeholder for NBA, UFC, etc.

    return render_template(
        "index.html",
        picks=picks,
        today=datetime.utcnow().strftime("%Y-%m-%d"),
        now=datetime.utcnow()
    )

if __name__ == "__main__":
    app.run(debug=True)
