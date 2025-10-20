from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_cors import CORS
import jwt
from functools import wraps
 # Phải import User từ đây để dùng trong token_required

# Khởi tạo db (phải ở ngoài factory)
db = SQLAlchemy()

# ==================================
# === HÀM KIỂM TRA TOKEN (VỊ TRÍ ĐÚNG) ===
# ==================================
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'error': 'Token không tồn tại!'}), 401

        try:
            # Giải mã token
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            # Lấy thông tin user từ token
            current_user = User.query.get(data['sub'])
            if not current_user:
                return jsonify({'error': 'User không tồn tại!'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token đã hết hạn!'}), 401
        except Exception as e:
            return jsonify({'error': 'Token không hợp lệ!', 'details': str(e)}), 401

        return f(current_user, *args, **kwargs)

    return decorated
# ==================================


def create_app(config_class=Config):
    """Factory function để tạo Flask app"""
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Cho phép CORS
    CORS(app)
    db.init_app(app)
    
    # Import và đăng ký Blueprints (Routes)
    from app.routes.auth_routes import bp as auth_bp
    from app.routes.face_routes import bp as face_bp
    from app.routes.ticket_routes import bp as ticket_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(face_bp)
    app.register_blueprint(ticket_bp)

    return app