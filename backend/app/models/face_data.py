from app import db
from datetime import datetime
import pickle

class FaceData(db.Model):
    __tablename__ = 'Face_Data'
    
    face_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id', ondelete='CASCADE'), unique=True, nullable=False)
    face_encoding = db.Column(db.LargeBinary, nullable=False)  # Vector khuôn mặt (128D)
    photo_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    entry_logs = db.relationship('EntryLog', backref='face_data')
    
    def set_encoding(self, encoding_array):
        """Lưu numpy array thành binary"""
        self.face_encoding = pickle.dumps(encoding_array)
    
    def get_encoding(self):
        """Lấy numpy array từ binary"""
        return pickle.loads(self.face_encoding)
    
    def to_dict(self):
        return {
            'face_id': self.face_id,
            'user_id': self.user_id,
            'photo_path': self.photo_path,
            'created_at': self.created_at.isoformat()
        }