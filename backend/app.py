import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas

from models import db, Pick
from scraper import run_scraper
from filters import is_game_final, line_moved_in_your_direction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instance/picks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'devkey')

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Scheduler: runs scraper at 10AM, 3PM, 6PM US/Eastern
def start_scheduler():
    scheduler = BackgroundScheduler(timezone='US/Eastern')
    scheduler.add_job(run_scraper, 'cron', hour=10, minute=0)
    scheduler.add_job(run_scraper, 'cron', hour=15, minute=0)
    scheduler.add_job(run_scraper, 'cron', hour=18, minute=0)
    scheduler.start()

start_scheduler()

with app.app_context():
    db.create_all()

@app.route('/ping')
def ping():
    return 'pong', 200

@app.route('/api/todays-picks', methods=['GET'])
def todays_picks():
    picks = Pick.query.all()
    return jsonify([p.to_dict() for p in picks])

@app.route('/api/scrape-now', methods=['GET'])
@jwt_required()
def manual_scrape():
    run_scraper()
    return jsonify(status='scraped'), 200

@app.route('/api/export/pdf', methods=['GET'])
@jwt_required()
def export_pdf():
    picks = [p.to_dict() for p in Pick.query.all()]
    buf = BytesIO()
    c = canvas.Canvas(buf)
    y = 800
    for p in picks:
        line = f"{p['matchup']} | {p['type']} | C:{p['confidence_score']} | W:{p['win_probability']} | {p.get('summary','')}"
        c.drawString(50, y, line)
        y -= 15
        if y < 50:
            c.showPage(); y = 800
    c.save(); buf.seek(0)
    return send_file(buf, mimetype='application/pdf', as_attachment=True, download_name='picks.pdf')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)