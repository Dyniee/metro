# import jwt
# import datetime
# import os
# from werkzeug.security import generate_password_hash, check_password_hash

# # === IMPORT THAY THẾ ===
# from app import db # Dùng instance DB thực
# from app.models.user import User # Dùng Model User thực tế
# # =======================

# # Lấy khóa bí mật (PHẢI TRÙNG VỚI KHÓA TRONG app/decorators.py)
# SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key_if_env_not_set')
# REFRESH_TOKEN_SECRET = os.environ.get('REFRESH_TOKEN_SECRET', 'another_secret_for_refresh')
# TOKEN_EXPIRATION_HOURS = 24 
# REFRESH_EXPIRATION_DAYS = 7


# # --- HÀM TẠO TOKEN NỘI BỘ ---

# def _generate_token(user_id, is_refresh=False):
#     """Tạo JWT. Access token hết hạn sau 24 giờ."""
#     expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=TOKEN_EXPIRATION_HOURS)
#     key = SECRET_KEY
#     token_type = 'access'
        
#     try:
#         payload = {
#             'exp': expiration,
#             'iat': datetime.datetime.utcnow(),
#             'user_id': user_id,
#             'type': token_type
#         }
#         return jwt.encode(payload, key, algorithm='HS256')
#     except Exception as e:
#         print(f"Error generating {token_type} token: {e}")
#         return None

# # --- DỊCH VỤ NGHIỆP VỤ (BUSINESS LOGIC) ---

# def register_user(username: str, password: str, email: str):
#     """
#     Đăng ký người dùng mới vào MySQL DB.
#     """
#     # 1. Kiểm tra email/username đã tồn tại
#     if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
#         raise ValueError("Tên người dùng hoặc Email đã tồn tại.")

#     try:
#         # 2. Tạo đối tượng User
#         new_user = User(
#             username=username,
#             email=email,
#             # Giả định User model có field password_hash
#             # và method set_password sẽ hash và gán giá trị
#             wallet_balance=0.0 # Giá trị ban đầu
#         )
#         new_user.set_password(password) # Giả định hàm này tồn tại trong Model

#         # 3. Lưu vào MySQL
#         db.session.add(new_user)
#         db.session.commit()
        
#         return new_user # Trả về đối tượng user đã lưu
        
#     except Exception as e:
#         db.session.rollback()
#         print(f"Lỗi DB khi đăng ký: {e}")
#         raise Exception("Không thể đăng ký do lỗi cơ sở dữ liệu.")


# def authenticate_user(email: str, password: str):
#     """
#     Xác thực người dùng bằng EMAIL trong MySQL DB.
#     """
#     # 1. Tìm người dùng bằng email
#     user = User.query.filter_by(email=email).first()
    
#     # 2. Kiểm tra tồn tại VÀ kiểm tra mật khẩu
#     # Giả định User model có method check_password
#     if user and user.check_password(password):
#         # 3. Tạo Access Token
#         access_token = _generate_token(user.user_id) # Giả định ID là user.user_id
        
#         if not access_token:
#              raise Exception("Lỗi tạo Access Token.")
            
#         return access_token
#     else:
#         # Lỗi: Không tìm thấy user hoặc mật khẩu không khớp
#         raise ValueError("Email hoặc mật khẩu không đúng.")


# def refresh_token(refresh_token: str):
#     """Xử lý làm mới token (Logic giả định)."""
#     # Logic này vẫn giữ nguyên là giả định
#     raise ValueError("Chức năng làm mới token chưa được triển khai hoàn chỉnh.")


# def get_user_details(user_id: int):
#     """Lấy chi tiết người dùng theo ID từ MySQL DB."""
#     # 1. Tìm user bằng user_id
#     user = User.query.get(user_id)
    
#     if user:
#         # Giả định User model có method to_dict()
#         return user.to_dict() 
#     return None
