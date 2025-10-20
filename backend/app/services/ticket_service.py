from app import db
from app.models import EntryLog, User, Station, Ticket, FaceData
from config import Config
from datetime import datetime, timedelta, timezone
from sqlalchemy import desc

# Import các service khác
from app.services.face_service import FaceService, convert_base64_to_bytes

class TicketService:
    
    # Bảng giá vé (giống bảng giá cũ)
    # Giả định giá vé dựa trên KHOẢNG CÁCH ID của ga
    FARE_TABLE = {
        1: 7000,    # 1 ga
        2: 9000,    # 2 ga
        3: 11000,   # 3 ga
        4: 13000,   # 4 ga
        5: 15000,   # 5+ ga
    }
    
    @staticmethod
    def calculate_fare(station_a_id, station_b_id):
        """Tính cước dựa trên số ga (Giả định ID ga là liên tiếp)"""
        distance = abs(int(station_b_id) - int(station_a_id))
        
        # Xác định số ga
        num_stations = distance if distance > 0 else 1
        
        # Lấy giá từ bảng
        if num_stations <= 1:
            fare = TicketService.FARE_TABLE[1]
        elif num_stations <= 2:
            fare = TicketService.FARE_TABLE[2]
        elif num_stations <= 3:
            fare = TicketService.FARE_TABLE[3]
        elif num_stations <= 4:
            fare = TicketService.FARE_TABLE[4]
        else:
            fare = TicketService.FARE_TABLE[5]
        
        return fare, num_stations

    @staticmethod
    def buy_ticket_service(user_id, station_from_id, station_to_id, valid_at_datetime_str, face_images_b64):
        """
        Logic Mua Vé Mới: (Cho Web Portal)
        1. Tính giá vé
        2. Kiểm tra/Đăng ký khuôn mặt (nếu user chưa có)
        3. Kiểm tra ví
        4. Trừ tiền
        5. Tạo vé
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return None, "Người dùng không tồn tại"

            # 1. Tính giá vé
            fare, num_stations = TicketService.calculate_fare(station_from_id, station_to_id)

            # 2. Kiểm tra/Đăng ký khuôn mặt
            # (Theo logic của bạn: chụp ảnh khi mua vé)
            if not user.face_data:
                print(f"User {user_id} chưa có khuôn mặt. Đang đăng ký...")
                if not face_images_b64:
                    return None, "Cần hình ảnh để đăng ký khuôn mặt cho lần mua đầu tiên"
                
                # Chuyển đổi ảnh đầu tiên (từ base64)
                image_data, error = convert_base64_to_bytes(face_images_b64[0])
                if error:
                    return None, f"Lỗi xử lý ảnh: {error}"
                
                # Gọi service đăng ký
                face_data, error = FaceService.register_face(user.user_id, image_data)
                if error:
                    return None, f"Lỗi đăng ký khuôn mặt: {error}"

            # 3. Kiểm tra ví
            if user.wallet_balance < fare:
                return None, f"Số dư không đủ. Cần {fare:,.0f} VNĐ, bạn chỉ có {user.wallet_balance:,.0f} VNĐ."

            # 4. Trừ tiền từ ví
            success, message = user.deduct_balance(fare)
            if not success:
                return None, message # Trả về lỗi nếu trừ thất bại

            # 5. Tạo vé
            # Chuyển đổi chuỗi thời gian (ISO format) từ frontend sang object datetime
            # Ví dụ: "2025-10-20T09:15:00"
            try:
                valid_datetime_obj = datetime.fromisoformat(valid_at_datetime_str)
            except ValueError:
                return None, "Định dạng Ngày Giờ không hợp lệ (cần chuẩn ISO)."

            new_ticket = Ticket(
                user_id=user.user_id,
                station_from_id=station_from_id,
                station_to_id=station_to_id,
                valid_at_datetime=valid_datetime_obj, # Lưu cả Ngày và Giờ
                status='NEW',
                purchase_price=fare
            )
            
            db.session.add(new_ticket)
            db.session.commit()
            
            print(f"✅ User {user_id} đã mua vé {new_ticket.ticket_id} thành công!")
            return new_ticket, None # Trả về vé đã tạo

        except Exception as e:
            db.session.rollback()
            return None, f"Lỗi máy chủ khi mua vé: {str(e)}"

    @staticmethod
    def check_ticket_service(kiosk_station_id, image_data):
        """
        Logic Kiểm Tra Vé: (Cho Kiosk)
        1. Nhận diện khuôn mặt
        2. Tìm vé hợp lệ (đúng ga, đúng giờ, chưa dùng)
        3. Đánh dấu vé đã dùng
        """
        try:
            # 1. Nhận diện khuôn mặt
            face_data, confidence, error = FaceService.recognize_face(image_data)
            
            if error or not face_data:
                return None, f"Khuôn mặt không hợp lệ. ({error or 'Không tìm thấy'})"
            
            user = face_data.user
            print(f"Nhận diện User: {user.username} (Độ chính xác: {confidence:.2f}%)")

            # 2. Tìm vé hợp lệ
            # Logic: Tìm vé của user này, cho ga này, trạng thái 'NEW',
            # và trong khoảng thời gian cho phép (ví dụ: 1 giờ trước và sau giờ vé)
            
            now = datetime.now(timezone.utc)
            time_window_start = now - timedelta(hours=1) # Cho phép trễ 1h
            time_window_end = now + timedelta(hours=1)   # Cho phép sớm 1h

            valid_ticket = Ticket.query.filter(
                Ticket.user_id == user.user_id,
                Ticket.station_from_id == kiosk_station_id,
                Ticket.status == 'NEW',
                Ticket.valid_at_datetime >= time_window_start,
                Ticket.valid_at_datetime <= time_window_end
            ).order_by(Ticket.valid_at_datetime).first() # Lấy vé sớm nhất

            # 3. Xử lý kết quả
            if valid_ticket:
                # Tìm thấy vé! Đánh dấu đã sử dụng (check-in)
                valid_ticket.mark_as_used()
                print(f"✅ Check-in thành công cho vé {valid_ticket.ticket_id}")
                return valid_ticket, None
            else:
                # Không tìm thấy vé
                print(f"❌ Check-in thất bại: Không tìm thấy vé hợp lệ cho User {user.user_id} tại Ga {kiosk_station_id}")
                return None, "Không tìm thấy vé hợp lệ"

        except Exception as e:
            return None, f"Lỗi máy chủ khi kiểm tra vé: {str(e)}"