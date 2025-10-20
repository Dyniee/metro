from app import db
from datetime import datetime

class Ticket(db.Model):
    __tablename__ = 'Tickets'
    
    ticket_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id', ondelete='CASCADE'), nullable=False)
    
    station_from_id = db.Column(db.Integer, db.ForeignKey('Stations.station_id'), nullable=False)
    station_to_id = db.Column(db.Integer, db.ForeignKey('Stations.station_id'), nullable=False)
    
    # === THAY ĐỔI THEO YÊU CẦU CỦA BẠN ===
    # Đổi từ Date (Ngày) sang DateTime (Ngày và Giờ)
    valid_at_datetime = db.Column(db.DateTime, nullable=False)
    # ====================================
    
    # Trạng thái: 'NEW' (Mới), 'USED' (Đã dùng), 'EXPIRED' (Hết hạn)
    status = db.Column(db.String(20), default='NEW', nullable=False)
    
    purchase_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # Ngày giờ mua vé
    
    # Relationships để lấy tên Ga
    station_from = db.relationship('Station', foreign_keys=[station_from_id])
    station_to = db.relationship('Station', foreign_keys=[station_to_id])
    
    def to_dict(self):
        return {
            'ticket_id': self.ticket_id,
            'user_id': self.user_id,
            'station_from_id': self.station_from_id,
            'station_from_name': self.station_from.station_name if self.station_from else None,
            'station_to_id': self.station_to_id,
            'station_to_name': self.station_to.station_name if self.station_to else None,
            
            # === CẬP NHẬT TRƯỜNG TRẢ VỀ ===
            'valid_at_datetime': self.valid_at_datetime.isoformat() if self.valid_at_datetime else None,
            # ===============================
            
            'status': self.status,
            'purchase_price': self.purchase_price,
            'created_at': self.created_at.isoformat()
        }

    def mark_as_used(self):
        """Đánh dấu vé này là đã sử dụng (khi Kiosk check-in)"""
        self.status = 'USED'
        db.session.commit()