from app import db
from datetime import datetime

class Station(db.Model):
    __tablename__ = 'Stations'
    
    station_id = db.Column(db.Integer, primary_key=True)
    station_name = db.Column(db.String(100), unique=True, nullable=False)
    line = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    entry_logs = db.relationship('EntryLog', backref='station')
    
    def to_dict(self):
        return {
            'station_id': self.station_id,
            'station_name': self.station_name,
            'line': self.line
        }