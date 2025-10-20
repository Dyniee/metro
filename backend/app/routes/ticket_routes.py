# from flask import Blueprint, request, jsonify
# from app.services import TicketService # Service mới
# from app.models import Station, EntryLog, User, Ticket
# from app import token_required # <-- IMPORT TỪ GÓI 'app' (tức là file __init__.py)
# from app import db
# from datetime import datetime

# bp = Blueprint('ticket', __name__, url_prefix='/api')

# # ==========================================
# # === API MUA VÉ (CHO WEB PORTAL) ===
# # ==========================================
# @bp.route('/ticket/buy', methods=['POST'])
# @token_required # <-- BẮT BUỘC PHẢI ĐĂNG NHẬP MỚI ĐƯỢC MUA
# def buy_ticket(current_user):
#     """
#     API để User mua vé (Web Portal)
#     Nhận: { station_from_id, station_to_id, valid_at_datetime, face_images: [...] }
#     Token sẽ xác định 'current_user'
#     """
#     data = request.get_json()
#     if not data:
#         return jsonify({'error': 'Không có dữ liệu JSON'}), 400

#     station_from_id = data.get('station_from_id')
#     station_to_id = data.get('station_to_id')
#     valid_at_datetime_str = data.get('valid_at_datetime') # VD: "2025-10-20T09:15:00"
#     face_images_b64 = data.get('face_images', []) # (Chỉ cần nếu user chưa có mặt)

#     # Validate
#     if not station_from_id or not station_to_id or not valid_at_datetime_str:
#         return jsonify({'error': 'Thiếu Ga đi, Ga đến hoặc Ngày Giờ'}), 400

#     # Gọi service
#     ticket, error = TicketService.buy_ticket_service(
#         user_id=current_user.user_id, # Lấy ID từ Token, an toàn hơn
#         station_from_id=station_from_id,
#         station_to_id=station_to_id,
#         valid_at_datetime_str=valid_at_datetime_str,
#         face_images_b64=face_images_b64
#     )

#     if error:
#         return jsonify({'error': error}), 400 # Lỗi 400 (Bad Request)

#     # Thành công
#     return jsonify({
#         'message': 'Mua vé thành công!',
#         'ticket': ticket.to_dict(),
#         'new_balance': current_user.wallet_balance # Trả về số dư mới
#     }), 201 # 201 (Created)

# # ==========================================
# # === API KIỂM TRA VÉ (CHO KIOSK) ===
# # ==========================================
# @bp.route('/kiosk/check', methods=['POST'])
# def kiosk_check():
#     """
#     API để Kiosk kiểm tra vé (không cần Token)
#     Nhận: FormData { station_id, image }
#     """
#     if 'image' not in request.files:
#         return jsonify({'error': 'Vui lòng upload ảnh', 'status': 'RED'}), 400
    
#     data = request.form
#     station_id = data.get('station_id')
    
#     if not station_id:
#         return jsonify({'error': 'Thiếu ID của Ga Kiosk', 'status': 'RED'}), 400
    
#     station = Station.query.get(station_id)
#     if not station:
#         return jsonify({'error': 'Ga Kiosk không tồn tại', 'status': 'RED'}), 404

#     try:
#         file = request.files['image']
#         image_data = file.read() # Đọc ảnh (dạng bytes)
        
#         # Gọi service kiểm tra
#         ticket, error = TicketService.check_ticket_service(
#             kiosk_station_id=station_id,
#             image_data=image_data
#         )
        
#         if error:
#             return jsonify({
#                 'error': error,
#                 'status': 'RED' # BÁO ĐỎ
#             }), 400
        
#         # THÀNH CÔNG (BÁO XANH)
#         return jsonify({
#             'message': 'Check-in thành công!',
#             'status': 'GREEN', # BÁO XANH
#             'user': ticket.user.to_dict(),
#             'ticket': ticket.to_dict()
#         }), 200
        
#     except Exception as e:
#         return jsonify({'error': f'Lỗi: {str(e)}', 'status': 'RED'}), 500

# # ==========================================
# # === API LẤY LỊCH SỬ VÉ (Cập nhật) ===
# # ==========================================
# @bp.route('/ticket/history', methods=['GET'])
# @token_required
# def get_history(current_user):
#     """Lấy lịch sử MUA VÉ của user đã đăng nhập"""
    
#     # Lấy tất cả vé của user này, sắp xếp mới nhất lên trước
#     tickets = Ticket.query.filter_by(user_id=current_user.user_id)\
#                         .order_by(Ticket.created_at.desc())\
#                         .all()
    
#     return jsonify({
#         'user': current_user.to_dict(),
#         'history': [t.to_dict() for t in tickets]
#     }), 200

# # ==========================================
# # === API LẤY DANH SÁCH GA (Giữ nguyên) ===
# # ==========================================
# @bp.route('/ticket/stations', methods=['GET'])
# def get_stations():
#     """Lấy danh sách tất cả ga"""
#     stations = Station.query.all()
#     return jsonify([s.to_dict() for s in stations]), 200

from flask import Blueprint, request, jsonify
from app.services import TicketService # Service mới
from app.models import Station, EntryLog, User, Ticket
from app import token_required # <-- IMPORT HÀM TỪ app/__init__.py
from app import db
from datetime import datetime
import json
import os

bp = Blueprint('ticket', __name__, url_prefix='/api')

# ==========================================
# === API MUA VÉ (CHO WEB PORTAL) ===
# ==========================================
@bp.route('/ticket/buy', methods=['POST'])
@token_required # BẮT BUỘC ĐĂNG NHẬP
def buy_ticket(current_user):
    """
    API để User mua vé (Web Portal)
    Nhận: { station_from_id, station_to_id, valid_at_datetime, face_images: [...] }
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Không có dữ liệu JSON'}), 400

    station_from_id = data.get('station_from_id')
    station_to_id = data.get('station_to_id')
    valid_at_datetime_str = data.get('valid_at_datetime')
    face_images_b64 = data.get('face_images', [])

    if not station_from_id or not station_to_id or not valid_at_datetime_str:
        return jsonify({'error': 'Thiếu Ga đi, Ga đến hoặc Ngày Giờ'}), 400

    # Gọi service
    ticket, error = TicketService.buy_ticket_service(
        user_id=current_user.user_id,
        station_from_id=station_from_id,
        station_to_id=station_to_id,
        valid_at_datetime_str=valid_at_datetime_str,
        face_images_b64=face_images_b64
    )

    if error:
        return jsonify({'error': error}), 400

    # Sau khi trừ tiền, cần tải lại thông tin user để trả về số dư mới nhất
    updated_user = User.query.get(current_user.user_id)
    
    return jsonify({
        'message': 'Mua vé thành công!',
        'ticket': ticket.to_dict(),
        'user': updated_user.to_dict(), # Trả về user với số dư mới
        'new_balance': updated_user.wallet_balance 
    }), 201

# ==========================================
# === API KIỂM TRA VÉ (CHO KIOSK) ===
# ==========================================
@bp.route('/kiosk/check', methods=['POST'])
def kiosk_check():
    """
    API để Kiosk kiểm tra vé (không cần Token)
    Nhận: FormData { station_id, image }
    """
    if 'image' not in request.files:
        return jsonify({'error': 'Vui lòng upload ảnh', 'status': 'RED'}), 400
    
    data = request.form
    station_id = data.get('station_id')
    
    if not station_id:
        return jsonify({'error': 'Thiếu ID của Ga Kiosk', 'status': 'RED'}), 400
    
    # Lấy thông tin ảnh dạng bytes
    file = request.files['image']
    image_data = file.read() 
        
    # Gọi service kiểm tra
    ticket, error = TicketService.check_ticket_service(
        kiosk_station_id=station_id,
        image_data=image_data
    )
    
    if error:
        return jsonify({
            'error': error,
            'status': 'RED'
        }), 400
    
    # THÀNH CÔNG (BÁO XANH)
    return jsonify({
        'message': 'Check-in thành công!',
        'status': 'GREEN',
        'user': ticket.user.to_dict(),
        'ticket': ticket.to_dict()
    }), 200

# ==========================================
# === API LẤY LỊCH SỬ VÉ (Cập nhật) ===
# ==========================================
@bp.route('/ticket/history', methods=['GET'])
@token_required
def get_history(current_user):
    """Lấy lịch sử MUA VÉ của user đã đăng nhập"""
    
    # Lấy tất cả vé của user này, sắp xếp mới nhất lên trước
    tickets = Ticket.query.filter_by(user_id=current_user.user_id)\
                        .order_by(Ticket.created_at.desc())\
                        .all()
    
    return jsonify({
        'user': current_user.to_dict(),
        'history': [t.to_dict() for t in tickets]
    }), 200

# ==========================================
# === API LẤY DANH SÁCH GA (Giữ nguyên) ===
# ==========================================
@bp.route('/ticket/stations', methods=['GET'])
def get_stations():
    """Lấy danh sách tất cả ga"""
    stations = Station.query.all()
    return jsonify([s.to_dict() for s in stations]), 200
