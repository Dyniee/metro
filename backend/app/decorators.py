# from functools import wraps
# from flask import request, jsonify
# import jwt
# # Import Config và User model
# from config import Config
# # Chú ý: Import User ở đây có thể gây lỗi circular nếu model User import db từ __init__. 
# # Chúng ta sẽ giữ nguyên cấu trúc import User bên trong decorator để giảm thiểu rủi ro.

# def token_required(f):
#     """
#     Decorator để bảo vệ routes bằng cách xác thực JWT.
#     Trích xuất đối tượng User từ token payload và truyền vào hàm route.
#     """
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         # Import User bên trong hàm để giải quyết vấn đề import vòng tròn
#         from app.models import User 
        
#         token = None
#         # Xử lý cả tiêu đề Authorization: Bearer và token đơn giản
#         if 'Authorization' in request.headers:
#             auth_header = request.headers['Authorization']
#             if auth_header.startswith('Bearer '):
#                  token = auth_header.split(" ")[1]
#             else:
#                  token = auth_header # Nếu chỉ gửi token trần
        
#         # Nếu token không được tìm thấy, kiểm tra trong Query Params (thường dùng cho web socket)
#         if not token and 'token' in request.args:
#             token = request.args.get('token')

#         if not token:
#             return jsonify({'error': 'Token không tồn tại!'}), 401

#         try:
#             # Token payload cũ của bạn dùng 'sub', chúng ta sẽ giữ nguyên
#             data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
#             user_id = data.get('sub') # Giả định 'sub' chứa user_id
            
#             if not user_id:
#                 raise jwt.InvalidTokenError("Token thiếu trường 'sub' (User ID).")
                
#             current_user = User.query.get(user_id)
            
#             if not current_user:
#                 return jsonify({'error': 'User không tồn tại!'}), 401
                
#         except jwt.ExpiredSignatureError:
#             return jsonify({'error': 'Token đã hết hạn!'}), 401
#         except Exception as e:
#             # Ghi log lỗi chi tiết cho debug
#             print(f"Lỗi xác thực JWT: {e}")
#             return jsonify({'error': 'Token không hợp lệ!', 'details': str(e)}), 401

#         # Truyền đối tượng User vào hàm route
#         return f(current_user, *args, **kwargs)

#     return decorated
