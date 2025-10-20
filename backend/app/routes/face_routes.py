# from flask import Blueprint, request, jsonify
# from app.services.face_service import register_face, verify_face # nếu bạn chỉ cần các hàm cụ thể
# from app.models import User, FaceData
# from app import db
# import os

# bp = Blueprint('face', __name__, url_prefix='/api/face')

# @bp.route('/register/<int:user_id>', methods=['POST'])
# def register_face(user_id):
#     """Đăng ký khuôn mặt cho user"""
#     user = User.query.get(user_id)
    
#     if not user:
#         return jsonify({'error': 'Người dùng không tồn tại'}), 404
    
#     # Kiểm tra file ảnh
#     if 'image' not in request.files:
#         return jsonify({'error': 'Vui lòng upload ảnh'}), 400
    
#     file = request.files['image']
#     if file.filename == '':
#         return jsonify({'error': 'File ảnh trống'}), 400
    
#     try:
#         # Đọc dữ liệu ảnh
#         image_data = file.read()
        
#         # Đăng ký khuôn mặt
#         face_data, error = FaceService.register_face(user_id, image_data, file.filename)
        
#         if error:
#             return jsonify({'error': error}), 400
        
#         return jsonify({
#             'message': 'Đăng ký khuôn mặt thành công',
#             'face_data': face_data.to_dict()
#         }), 201
        
#     except Exception as e:
#         return jsonify({'error': f'Lỗi: {str(e)}'}), 500

# @bp.route('/recognize', methods=['POST'])
# def recognize():
#     """Nhận diện khuôn mặt"""
#     if 'image' not in request.files:
#         return jsonify({'error': 'Vui lòng upload ảnh'}), 400
    
#     file = request.files['image']
#     if file.filename == '':
#         return jsonify({'error': 'File ảnh trống'}), 400
    
#     try:
#         image_data = file.read()
#         face_data, confidence, error = FaceService.recognize_face(image_data)
        
#         if error:
#             return jsonify({
#                 'error': error,
#                 'confidence': confidence
#             }), 400
        
#         user = face_data.user
        
#         return jsonify({
#             'message': 'Nhận diện thành công',
#             'user': user.to_dict(),
#             'face_id': face_data.face_id,
#             'confidence': f'{confidence:.2f}%'
#         }), 200
        
#     except Exception as e:
#         return jsonify({'error': f'Lỗi: {str(e)}'}), 500

# @bp.route('/user/<int:user_id>', methods=['GET'])
# def get_face_data(user_id):
#     """Lấy dữ liệu khuôn mặt của user"""
#     face_data = FaceData.query.filter_by(user_id=user_id).first()
    
#     if not face_data:
#         return jsonify({'error': 'Chưa đăng ký khuôn mặt'}), 404
    
#     return jsonify(face_data.to_dict()), 200

from flask import Blueprint, request, jsonify
from app.services import FaceService
from app.models import User, FaceData
from app import db
import os

bp = Blueprint('face', __name__, url_prefix='/api/face')

@bp.route('/register/<int:user_id>', methods=['POST'])
def register_face(user_id):
    """Đăng ký khuôn mặt cho user"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Người dùng không tồn tại'}), 404
    
    # Kiểm tra file ảnh
    if 'image' not in request.files:
        return jsonify({'error': 'Vui lòng upload ảnh'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'File ảnh trống'}), 400
    
    try:
        # Đọc dữ liệu ảnh
        image_data = file.read()
        
        # Đăng ký khuôn mặt
        face_data, error = FaceService.register_face(user_id, image_data, file.filename)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Đăng ký khuôn mặt thành công',
            'face_data': face_data.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500

@bp.route('/recognize', methods=['POST'])
def recognize():
    """Nhận diện khuôn mặt"""
    if 'image' not in request.files:
        return jsonify({'error': 'Vui lòng upload ảnh'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'File ảnh trống'}), 400
    
    try:
        image_data = file.read()
        face_data, confidence, error = FaceService.recognize_face(image_data)
        
        if error:
            return jsonify({
                'error': error,
                'confidence': confidence
            }), 400
        
        user = face_data.user
        
        return jsonify({
            'message': 'Nhận diện thành công',
            'user': user.to_dict(),
            'face_id': face_data.face_id,
            'confidence': f'{confidence:.2f}%'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500

@bp.route('/user/<int:user_id>', methods=['GET'])
def get_face_data(user_id):
    """Lấy dữ liệu khuôn mặt của user"""
    face_data = FaceData.query.filter_by(user_id=user_id).first()
    
    if not face_data:
        return jsonify({'error': 'Chưa đăng ký khuôn mặt'}), 404
    
    return jsonify(face_data.to_dict()), 200