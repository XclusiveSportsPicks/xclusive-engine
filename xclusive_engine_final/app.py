from dotenv import load_dotenv
import os
from flask import Flask, render_template, request
from datetime import datetime
from mlb.engine import get_today_mlb_picks

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    league = request.args.get("league", "MLB")
    
    if league == "MLB":
        picks = get_today_mlb_picks()
    # elif league == "NBA":
    #     picks = get_today_nba_picks()
    # elif league == "UFC":
    #     picks = get_today_ufc_picks()
    else:
        picks = []

    return render_template("index.html", picks=picks, today=datetime.utcnow().strftime("%Y-%m-%d"), now=datetime.utcnow())
