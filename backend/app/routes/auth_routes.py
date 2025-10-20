# from flask import Blueprint, request, jsonify
# from app import db, Config
# from app.models import User
# from datetime import datetime, timedelta, timezone
# import jwt # <-- Thư viện Token vừa cài
# from werkzeug.security import check_password_hash # (User model đã import cái generate)

# bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# # ==========================================
# # === API ĐĂNG KÝ (Đã cập nhật) ===
# # ==========================================
# @bp.route('/register', methods=['POST'])
# def register():
#     """Đăng ký tài khoản mới (có password và nạp tiền ban đầu)"""
#     data = request.get_json()
    
#     username = data.get('username')
#     email = data.get('email')
#     password = data.get('password') 
#     phone = data.get('phone')
#     initial_balance = float(data.get('initial_balance', 0)) # <-- LẤY LẠI DÒNG NÀY

#     # Validate
#     if not username or not email or not password:
#         return jsonify({'error': 'Username, email và password bắt buộc'}), 400
    
#     # Kiểm tra user đã tồn tại
#     if User.query.filter_by(username=username).first():
#         return jsonify({'error': 'Username đã tồn tại'}), 409
    
#     if User.query.filter_by(email=email).first():
#         return jsonify({'error': 'Email đã tồn tại'}), 409
    
#     try:
#         user = User(
#             username=username,
#             email=email,
#             phone=phone,
#             wallet_balance=initial_balance  # <-- GÁN SỐ DƯ BAN ĐẦU
#         )
#         user.set_password(password) # Mã hóa và lưu password
        
#         db.session.add(user)
#         db.session.commit()
        
#         return jsonify({
#             'message': 'Đăng ký thành công',
#             'user': user.to_dict()
#         }), 201
        
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': f'Lỗi: {str(e)}'}), 500

# # ==========================================
# # === API ĐĂNG NHẬP (MỚI) ===
# # ==========================================
# @bp.route('/login', methods=['POST'])
# def login():
#     """Đăng nhập và trả về JWT Token"""
#     data = request.get_json()
    
#     email = data.get('email')
#     password = data.get('password')
    
#     if not email or not password:
#         return jsonify({'error': 'Email và password bắt buộc'}), 400
        
#     # Tìm user bằng email (email là duy nhất)
#     user = User.query.filter_by(email=email).first()
    
#     # Kiểm tra user tồn tại VÀ check password
#     if user is None or not user.check_password(password):
#         return jsonify({'error': 'Email hoặc password không chính xác'}), 401 # Lỗi 401 Unauthorized
        
#     # Nếu đúng -> Tạo Token
#     try:
#         # Token sẽ chứa user_id và hết hạn sau 1 ngày
#         token_payload = {
#             'sub': user.user_id, # Subject (ID của user)
#             'iat': datetime.now(timezone.utc), # Issued At (Thời gian tạo)
#             'exp': datetime.now(timezone.utc) + timedelta(days=1) # Expiration (Hết hạn)
#         }
        
#         # Tạo token
#         token = jwt.encode(
#             token_payload,
#             Config.SECRET_KEY, # Dùng SECRET_KEY từ config.py
#             algorithm='HS256'
#         )
        
#         return jsonify({
#             'message': 'Đăng nhập thành công',
#             'token': token,
#             'user': user.to_dict()
#         }), 200
        
#     except Exception as e:
#         return jsonify({'error': f'Lỗi tạo token: {str(e)}'}), 500

# # ==========================================
# # === API LẤY THÔNG TIN USER (Giữ nguyên) ===
# # ==========================================
# @bp.route('/user/<int:user_id>', methods=['GET'])
# def get_user(user_id):
#     """Lấy thông tin user (bao gồm cả face_data)"""
#     user = User.query.get(user_id)
    
#     if not user:
#         return jsonify({'error': 'Người dùng không tồn tại'}), 404
    
#     # === THÊM LOGIC TRẢ VỀ FACE_DATA ===
#     user_data = user.to_dict()
#     # Kiểm tra xem user có face_data không và thêm vào dict trả về
#     if user.face_data:
#         user_data['face_data'] = user.face_data.to_dict() # Trả về thông tin face_data
#     else:
#         user_data['face_data'] = None
#     return jsonify(user_data), 200
# # ==========================================
# # === API NẠP TIỀN VÀO VÍ (Giữ nguyên) ===
# # ==========================================
# @bp.route('/user/<int:user_id>/balance', methods=['POST'])
# def add_balance(user_id):
#     """Nạp tiền vào ví"""
#     user = User.query.get(user_id)
    
#     if not user:
#         return jsonify({'error': 'Người dùng không tồn tại'}), 404
    
#     data = request.get_json()
#     amount = float(data.get('amount', 0))
    
#     if amount <= 0:
#         return jsonify({'error': 'Số tiền phải lớn hơn 0'}), 400
    
#     try:
#         # Dùng hàm 'add_balance' trong model
#         success, message = user.add_balance(amount)
#         if not success:
#             return jsonify({'error': message}), 400
            
#         return jsonify({
#             'message': 'Nạp tiền thành công',
#             'new_balance': user.wallet_balance
#         }), 200
#     except Exception as e:
#         return jsonify({'error': f'Lỗi: {str(e)}'}), 500
from flask import Blueprint, request, jsonify
from app import db, Config
from app.models import User
from datetime import datetime, timedelta, timezone
import jwt # <-- Thư viện Token vừa cài
from werkzeug.security import check_password_hash # (User model đã import cái generate)

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# ==========================================
# === API ĐĂNG KÝ (Đã cập nhật) ===
# ==========================================
@bp.route('/register', methods=['POST'])
def register():
    """Đăng ký tài khoản mới (có password và nạp tiền ban đầu)"""
    data = request.get_json()
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password') 
    phone = data.get('phone')
    initial_balance = float(data.get('initial_balance', 0)) # <-- LẤY LẠI DÒNG NÀY

    # Validate
    if not username or not email or not password:
        return jsonify({'error': 'Username, email và password bắt buộc'}), 400
    
    # Kiểm tra user đã tồn tại
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username đã tồn tại'}), 409
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email đã tồn tại'}), 409
    
    try:
        user = User(
            username=username,
            email=email,
            phone=phone,
            wallet_balance=initial_balance  # <-- GÁN SỐ DƯ BAN ĐẦU
        )
        user.set_password(password) # Mã hóa và lưu password
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Đăng ký thành công',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500

# ==========================================
# === API ĐĂNG NHẬP (MỚI) ===
# ==========================================
@bp.route('/login', methods=['POST'])
def login():
    """Đăng nhập và trả về JWT Token"""
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email và password bắt buộc'}), 400
        
    # Tìm user bằng email (email là duy nhất)
    user = User.query.filter_by(email=email).first()
    
    # Kiểm tra user tồn tại VÀ check password
    if user is None or not user.check_password(password):
        return jsonify({'error': 'Email hoặc password không chính xác'}), 401 # Lỗi 401 Unauthorized
        
    # Nếu đúng -> Tạo Token
    try:
        # Token sẽ chứa user_id và hết hạn sau 1 ngày
        token_payload = {
            'sub': user.user_id, # Subject (ID của user)
            'iat': datetime.now(timezone.utc), # Issued At (Thời gian tạo)
            'exp': datetime.now(timezone.utc) + timedelta(days=1) # Expiration (Hết hạn)
        }
        
        # Tạo token
        token = jwt.encode(
            token_payload,
            Config.SECRET_KEY, # Dùng SECRET_KEY từ config.py
            algorithm='HS256'
        )
        
        return jsonify({
            'message': 'Đăng nhập thành công',
            'token': token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Lỗi tạo token: {str(e)}'}), 500

# ==========================================
# === API LẤY THÔNG TIN USER (Giữ nguyên) ===
# ==========================================
@bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Lấy thông tin user"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Người dùng không tồn tại'}), 404
    
    return jsonify(user.to_dict()), 200

# ==========================================
# === API NẠP TIỀN VÀO VÍ (Giữ nguyên) ===
# ==========================================
@bp.route('/user/<int:user_id>/balance', methods=['POST'])
def add_balance(user_id):
    """Nạp tiền vào ví"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Người dùng không tồn tại'}), 404
    
    data = request.get_json()
    amount = float(data.get('amount', 0))
    
    if amount <= 0:
        return jsonify({'error': 'Số tiền phải lớn hơn 0'}), 400
    
    try:
        # Dùng hàm 'add_balance' trong model
        success, message = user.add_balance(amount)
        if not success:
            return jsonify({'error': message}), 400
            
        return jsonify({
            'message': 'Nạp tiền thành công',
            'new_balance': user.wallet_balance
        }), 200
    except Exception as e:
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500