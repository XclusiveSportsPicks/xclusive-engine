# app.py

from dotenv import load_dotenv
import os
from flask import Flask, render_template, request
from datetime import datetime
from mlb.engine import get_today_mlb_picks  # ✅ Corrected import

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", "xclusive-dev-key")

@app.route("/")
def index():
    league = request.args.get("league", "MLB")

    if league == "MLB":
        picks = get_today_mlb_picks()
    else:
        picks = []

    return render_template(
        "index.html",
        picks=picks,
        today=datetime.utcnow().strftime("%Y-%m-%d"),
        now=datetime.utcnow()
    )

if __name__ == "__main__":
    app.run(debug=True)
