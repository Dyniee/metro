# from app import db
# from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash # <-- Phải có dòng này

# class User(db.Model):
#     __tablename__ = 'Users'
    
#     user_id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     phone = db.Column(db.String(20))
    
#     password_hash = db.Column(db.String(256), nullable=False)
#     wallet_balance = db.Column(db.Float, default=0, nullable=False)
    
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
#     # Relationships
#     face_data = db.relationship('FaceData', backref='user', uselist=False, cascade='all, delete-orphan')
#     tickets = db.relationship('Ticket', backref='user', cascade='all, delete-orphan')
#     entry_logs = db.relationship('EntryLog', backref='user', cascade='all, delete-orphan')
    
#     # ========================================
#     # === HÀM BỊ THIẾU CỦA BẠN LÀ ĐÂY ===
#     # ========================================
#     def set_password(self, password):
#         """Tạo hash cho password"""
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         """Kiểm tra hash của password"""
#         return check_password_hash(self.password_hash, password)
#     # ========================================
    
#     # === HÀM XỬ LÝ VÍ ===
#     def add_balance(self, amount):
#         """Nạp tiền vào ví"""
#         if amount <= 0:
#             return False, "Số tiền nạp phải lớn hơn 0"
#         self.wallet_balance += amount
#         db.session.commit()
#         return True, "Nạp tiền thành công"

#     def deduct_balance(self, amount):
#         """Trừ tiền từ ví (dùng khi mua vé)"""
#         if amount <= 0:
#             return False, "Số tiền trừ phải lớn hơn 0"
#         if self.wallet_balance < amount:
#             return False, "Số dư trong ví không đủ"
            
#         self.wallet_balance -= amount
#         db.session.commit()
#         return True, "Thanh toán thành công"
    
#     def to_dict(self):
#         return {
#             'user_id': self.user_id,
#             'username': self.username,
#             'email': self.email,
#             'phone': self.phone,
#             'wallet_balance': self.wallet_balance,
#             'created_at': self.created_at.isoformat()
#         }

# from app import db
# from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash
# import jwt
# from config import Config

# class User(db.Model):
#     __tablename__ = 'Users'
    
#     user_id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password_hash = db.Column(db.String(255), nullable=False)  # ✅ Thêm mật khẩu
#     phone = db.Column(db.String(20))
#     wallet_balance = db.Column(db.Float, default=0)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
#     # Relationships
#     face_data = db.relationship('FaceData', backref='user', uselist=False, cascade='all, delete-orphan')
#     tickets = db.relationship('Ticket', backref='user', cascade='all, delete-orphan')
#     entry_logs = db.relationship('EntryLog', backref='user', cascade='all, delete-orphan')
    
#     def set_password(self, password):
#         """Hash và lưu mật khẩu"""
#         self.password_hash = generate_password_hash(password)
    
#     def check_password(self, password):
#         """Kiểm tra mật khẩu"""
#         return check_password_hash(self.password_hash, password)
    
#     def generate_token(self):
#         """Tạo JWT token"""
#         token = jwt.encode(
#             {'sub': self.user_id},
#             Config.SECRET_KEY,
#             algorithm="HS256"
#         )
#         return token
    
#     def to_dict(self):
#         return {
#             'user_id': self.user_id,
#             'username': self.username,
#             'email': self.email,
#             'phone': self.phone,
#             'wallet_balance': self.wallet_balance,
#             'created_at': self.created_at.isoformat()
#         }
    
#     def add_balance(self, amount):
#         self.wallet_balance += amount
#         db.session.commit()
    
#     def deduct_balance(self, amount):
#         if self.wallet_balance >= amount:
#             self.wallet_balance -= amount
#             db.session.commit()
#             return True
#         return False

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash # <-- Phải có dòng này

class User(db.Model):
    __tablename__ = 'Users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    
    password_hash = db.Column(db.String(256), nullable=False)
    wallet_balance = db.Column(db.Float, default=0, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    face_data = db.relationship('FaceData', backref='user', uselist=False, cascade='all, delete-orphan')
    tickets = db.relationship('Ticket', backref='user', cascade='all, delete-orphan')
    entry_logs = db.relationship('EntryLog', backref='user', cascade='all, delete-orphan')
    
    # ========================================
    # === HÀM BỊ THIẾU CỦA BẠN LÀ ĐÂY ===
    # ========================================
    def set_password(self, password):
        """Tạo hash cho password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Kiểm tra hash của password"""
        return check_password_hash(self.password_hash, password)
    # ========================================
    
    # === HÀM XỬ LÝ VÍ ===
    def add_balance(self, amount):
        """Nạp tiền vào ví"""
        if amount <= 0:
            return False, "Số tiền nạp phải lớn hơn 0"
        self.wallet_balance += amount
        db.session.commit()
        return True, "Nạp tiền thành công"

    def deduct_balance(self, amount):
        """Trừ tiền từ ví (dùng khi mua vé)"""
        if amount <= 0:
            return False, "Số tiền trừ phải lớn hơn 0"
        if self.wallet_balance < amount:
            return False, "Số dư trong ví không đủ"
            
        self.wallet_balance -= amount
        db.session.commit()
        return True, "Thanh toán thành công"
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'wallet_balance': self.wallet_balance,
            'created_at': self.created_at.isoformat()
        }