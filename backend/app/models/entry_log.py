from app import db
from datetime import datetime

class EntryLog(db.Model):
    __tablename__ = 'Entry_Logs'
    
    log_id = db.Column(db.Integer, primary_key=True)
    face_id = db.Column(db.Integer, db.ForeignKey('Face_Data.face_id'), nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey('Stations.station_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    action = db.Column(db.String(20), nullable=False)  # tap_in, tap_out
    confidence = db.Column(db.Float, nullable=False)
    fee_charged = db.Column(db.Float, default=0)
    
    def to_dict(self):
        return {
            'log_id': self.log_id,
            'face_id': self.face_id,
            'user_id': self.user_id,
            'station_id': self.station_id,
            'station_name': self.station.station_name if self.station else None,
            'timestamp': self.timestamp.isoformat(),
            'action': self.action,
            'confidence': self.confidence,
            'fee_charged': self.fee_charged
        }