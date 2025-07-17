# backend/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pick(db.Model):
    __tablename__ = 'picks'
    id                  = db.Column(db.Integer, primary_key=True)
    type                = db.Column(db.String(20), nullable=False)
    matchup             = db.Column(db.String(100), nullable=False)
    side                = db.Column(db.String(20), nullable=True)
    total_line          = db.Column(db.Float, nullable=True)
    spread_line         = db.Column(db.Float, nullable=True)
    odds_american       = db.Column(db.Integer, nullable=True)
    model_edge          = db.Column(db.Float, nullable=False, default=0.0)
    sharp_pct           = db.Column(db.Float, nullable=False, default=0.0)
    bet_pct             = db.Column(db.Float, nullable=False, default=0.0)
    line_movement_score = db.Column(db.Float, nullable=False, default=0.0)
    open_odds           = db.Column(db.Float, nullable=True)
    current_odds        = db.Column(db.Float, nullable=True)
    iso                 = db.Column(db.Float, nullable=True, default=0.0)
    pitcher_edge        = db.Column(db.Float, nullable=True, default=0.0)
    confidence_score    = db.Column(db.Float, nullable=True, default=0.0)
    win_probability     = db.Column(db.Float, nullable=True, default=0.0)
    summary             = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'matchup': self.matchup,
            'side': self.side,
            'total_line': self.total_line,
            'spread_line': self.spread_line,
            'odds_american': self.odds_american,
            'model_edge': self.model_edge,
            'sharp_pct': self.sharp_pct,
            'bet_pct': self.bet_pct,
            'line_movement_score': self.line_movement_score,
            'open_odds': self.open_odds,
            'current_odds': self.current_odds,
            'iso': self.iso,
            'pitcher_edge': self.pitcher_edge,
            'confidence_score': self.confidence_score,
            'win_probability': self.win_probability,
            'summary': self.summary
        }
