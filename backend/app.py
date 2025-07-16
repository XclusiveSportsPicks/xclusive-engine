from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import db, Pick
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas

from scraper import run_scraper, schedule_jobs

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///picks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/ping")
def ping():
    return "pong", 200

@app.route('/api/scrape-now', methods=['GET'])
def manual_scrape():
    result = run_scraper()
    return jsonify(result), 200

def process_picks(picks):
    results = []
    for p in picks:
        if p.type == 'pitcher' and (p.pitcher_edge or 0) < 2.0:
            continue
        if p.type == 'hitter':
            if not (p.iso >= 0.2 and p.sharp_pct >= p.bet_pct + 25):
                continue
        cs = ((p.model_edge/3.0)*0.5 +
              (p.sharp_pct/100.0)*0.3 +
              p.line_movement_score*0.2) * 10
        p.confidence_score = round(cs, 1)
        wp = ((p.confidence_score/10.0)*0.6 +
              (p.sharp_pct/100.0)*0.3 +
              p.line_movement_score*0.1) * 100
        p.win_probability = round(wp, 1)
        results.append(p)
    return sorted(results, key=lambda x: x.confidence_score, reverse=True)

@app.route('/api/todays-picks', methods=['GET'])
def todays_picks():
    picks = Pick.query.all()
    processed = process_picks(picks)
    return jsonify([{
        'id': p.id,
        'matchup': p.matchup,
        'type': p.type,
        'model_edge': p.model_edge,
        'sharp_pct': p.sharp_pct,
        'bet_pct': p.bet_pct,
        'line_movement_score': p.line_movement_score,
        'iso': p.iso,
        'pitcher_edge': p.pitcher_edge,
        'summary': p.summary,
        'confidence_score': p.confidence_score,
        'win_probability': p.win_probability
    } for p in processed])

@app.route('/api/picks', methods=['POST'])
def create_pick():
    data = request.json
    pick = Pick(**data)
    db.session.add(pick)
    db.session.commit()
    return jsonify({'id': pick.id}), 201

@app.route('/api/picks/<int:pk>', methods=['PUT','DELETE'])
def modify_pick(pk):
    pick = Pick.query.get_or_404(pk)
    if request.method == 'PUT':
        for k, v in request.json.items():
            setattr(pick, k, v)
        db.session.commit()
        return jsonify({'status': 'updated'})
    db.session.delete(pick)
    db.session.commit()
    return jsonify({'status': 'deleted'})

@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    picks = process_picks(Pick.query.all())
    df = pd.DataFrame([{
        'id': p.id,
        'matchup': p.matchup,
        'type': p.type,
        'model_edge': p.model_edge,
        'sharp_pct': p.sharp_pct,
        'bet_pct': p.bet_pct,
        'line_movement_score': p.line_movement_score,
        'iso': p.iso,
        'pitcher_edge': p.pitcher_edge,
        'summary': p.summary,
        'confidence_score': p.confidence_score,
        'win_probability': p.win_probability
    } for p in picks])
    buf = BytesIO()
    df.to_csv(buf, index=False)
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name='picks.csv', mimetype='text/csv')

@app.route('/api/export/pdf', methods=['GET'])
def export_pdf():
    picks = process_picks(Pick.query.all())
    buf = BytesIO()
    c = canvas.Canvas(buf)
    y = 800
    for p in picks:
        line = (
            f"{p.id}, {p.matchup}, {p.type}, Edge:{p.model_edge}, "
            f"Sharp%:{p.sharp_pct}, Bet%:{p.bet_pct}, Line:{p.line_movement_score}, "
            f"ISO:{p.iso}, PitcherEdge:{p.pitcher_edge}, "
            f"C:{p.confidence_score}, W:{p.win_probability}, Summary:{p.summary}"
        )
        c.drawString(50, y, line)
        y -= 15
        if y < 50:
            c.showPage()
            y = 800
    c.save()
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name='picks.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    schedule_jobs(app)
    port = int(os.getenv('PORT', 5000))
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint:20s} -> {rule.rule}")
    app.run(host='0.0.0.0', port=port, debug=True)

