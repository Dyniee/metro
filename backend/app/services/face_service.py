# import face_recognition
# import numpy as np
# from app import db
# from app.models import FaceData, User
# from config import Config
# import os
# from PIL import Image
# import io
# import base64
# import uuid  # <-- THÊM THƯ VIỆN NÀY ĐỂ TẠO TÊN FILE DUY NHẤT

# # Hàm này bạn đã thêm ở bước trước, giữ nguyên nó
# def convert_base64_to_bytes(b64_string):
#     """
#     Chuyển đổi chuỗi base64 (có tiền tố 'data:image/jpeg;base64,') thành bytes.
#     """
#     try:
#         if ',' in b64_string:
#             header, data = b64_string.split(',', 1)
#         else:
#             data = b64_string
        
#         data = data.ljust(len(data) + (4 - len(data) % 4) % 4, '=')
        
#         image_data = base64.b64decode(data)
#         return image_data, None
#     except Exception as e:
#         return None, f"Lỗi giải mã base64: {str(e)}"


# class FaceService:
    
#     @staticmethod
#     def extract_face_encoding(image_data):
#         """Trích xuất encoding từ ảnh (đầu vào là bytes)"""
#         try:
#             # Đọc ảnh từ dữ liệu bytes
#             image = Image.open(io.BytesIO(image_data))
            
#             # Chuyển đổi sang RGB nếu cần (quan trọng)
#             if image.mode != 'RGB':
#                 image = image.convert('RGB')
                
#             image_array = np.array(image)
            
#             # Tìm khuôn mặt
#             face_locations = face_recognition.face_locations(image_array)
            
#             if len(face_locations) == 0:
#                 return None, "Không tìm thấy khuôn mặt"
            
#             if len(face_locations) > 1:
#                 return None, "Ảnh có nhiều hơn 1 người"
            
#             # Trích xuất encoding
#             face_encodings = face_recognition.face_encodings(image_array, face_locations)
            
#             if len(face_encodings) == 0:
#                 return None, "Không thể trích xuất khuôn mặt"
            
#             return face_encodings[0], None
            
#         except Exception as e:
#             return None, f"Lỗi xử lý ảnh: {str(e)}"
    
#     # ===================================================================
#     # ===== HÀM NÀY ĐÃ ĐƯỢC CẬP NHẬT ĐỂ LƯU FILE ẢNH =====
#     # ===================================================================
#     @staticmethod
#     def register_face(user_id, image_data, photo_path=None):
#         """
#         Đăng ký khuôn mặt cho user.
#         Đầu vào 'image_data' là dữ liệu bytes của ảnh.
#         """
        
#         # 1. Trích xuất vector (encoding) từ dữ liệu bytes
#         encoding, error = FaceService.extract_face_encoding(image_data)
        
#         if error:
#             return None, error
        
#         try:
#             # 2. Lưu file ảnh vào thư mục /app/static/uploads
            
#             # Tạo một tên file duy nhất (ví dụ: 1a2b3c4d.jpg)
#             if not photo_path:
#                 filename = f"{uuid.uuid4().hex[:10]}.jpg"
#                 # Đảm bảo thư mục 'uploads' tồn tại
#                 upload_dir = os.path.join('app', 'static', 'uploads')
#                 os.makedirs(upload_dir, exist_ok=True)
                
#                 # Đường dẫn đầy đủ để lưu file
#                 save_path = os.path.join(upload_dir, filename)
                
#                 # Đường dẫn tương đối để lưu vào DB (vd: uploads/1a2b3c4d.jpg)
#                 db_photo_path = os.path.join('uploads', filename)
#             else:
#                 # Nếu có truyền tên file (trường hợp cũ), giữ nguyên
#                 save_path = os.path.join('app', 'static', 'uploads', photo_path)
#                 db_photo_path = os.path.join('uploads', photo_path)

#             # Ghi dữ liệu bytes của ảnh ra file
#             with open(save_path, 'wb') as f:
#                 f.write(image_data)
            
#             print(f"✅ Đã lưu file ảnh tại: {save_path}")

#             # 3. Kiểm tra user đã đăng ký khuôn mặt chưa (xóa cái cũ nếu có)
#             existing = FaceData.query.filter_by(user_id=user_id).first()
#             if existing:
#                 # Xóa file ảnh cũ (nếu có)
#                 if existing.photo_path:
#                     old_path = os.path.join('app', 'static', existing.photo_path)
#                     if os.path.exists(old_path):
#                         os.remove(old_path)
#                 db.session.delete(existing)
            
#             # 4. Tạo record mới trong DB
#             face_data = FaceData(user_id=user_id, photo_path=db_photo_path)
#             face_data.set_encoding(encoding) # Lưu vector
            
#             db.session.add(face_data)
#             db.session.commit()
            
#             print(f"✅ Đã lưu vector và đường dẫn ảnh vào DB cho User {user_id}")
            
#             return face_data, None
            
#         except Exception as e:
#             db.session.rollback()
#             return None, f"Lỗi đăng ký: {str(e)}"
#     # ===================================================================

    
#     @staticmethod
#     def recognize_face(image_data):
#         """Nhận diện khuôn mặt (đầu vào là bytes)"""
        
#         # 1. Trích xuất vector của ảnh đầu vào
#         encoding, error = FaceService.extract_face_encoding(image_data)
        
#         if error:
#             return None, 0, error
        
#         try:
#             # 2. Lấy tất cả face encodings (vector) từ database
#             all_faces = FaceData.query.all()
            
#             if not all_faces:
#                 return None, 0, "Chưa có khuôn mặt nào được đăng ký"
            
#             # 3. So sánh khuôn mặt
#             stored_encodings = [f.get_encoding() for f in all_faces]
#             distances = face_recognition.face_distance(stored_encodings, encoding)
            
#             min_distance_idx = np.argmin(distances)
#             min_distance = distances[min_distance_idx]
            
#             # Tính confidence (1 - distance)
#             confidence = max(0, 1 - min_distance) * 100
            
#             if confidence < Config.FACE_CONFIDENCE_THRESHOLD * 100:
#                 return None, confidence, f"Confidence thấp: {confidence:.2f}%"
            
#             face_data = all_faces[min_distance_idx]
#             return face_data, confidence, None
            
#         except Exception as e:
#             return None, 0, f"Lỗi nhận diện: {str(e)}"
# face_service.py (Đã dịch sang tiếng Việt để mô tả)
import face_recognition
import numpy as np
from app import db
from app.models import FaceData, User
from config import Config
import os
from PIL import Image
import io
import base64
import uuid  # <-- THÊM THƯ VIỆN NÀY ĐỂ TẠO TÊN FILE DUY NHẤT

# Hàm này bạn đã thêm ở bước trước, giữ nguyên nó
def convert_base64_to_bytes(b64_string):
    """
    Chuyển đổi chuỗi base64 (có tiền tố 'data:image/jpeg;base64,') thành bytes.
    """
    try:
        if ',' in b64_string:
            header, data = b64_string.split(',', 1)
        else:
            data = b64_string
        
        data = data.ljust(len(data) + (4 - len(data) % 4) % 4, '=')
        
        image_data = base64.b64decode(data)
        return image_data, None
    except Exception as e:
        return None, f"Lỗi giải mã base64: {str(e)}"


class FaceService:
    
    @staticmethod
    def extract_face_encoding(image_data):
        """Trích xuất encoding từ ảnh (đầu vào là bytes)"""
        try:
            # Đọc ảnh từ dữ liệu bytes
            image = Image.open(io.BytesIO(image_data))
            
            # Chuyển đổi sang RGB nếu cần (quan trọng)
            if image.mode != 'RGB':
                image = image.convert('RGB')
                
            image_array = np.array(image)
            
            # Tìm khuôn mặt
            face_locations = face_recognition.face_locations(image_array)
            
            if len(face_locations) == 0:
                return None, "Không tìm thấy khuôn mặt"
            
            if len(face_locations) > 1:
                return None, "Ảnh có nhiều hơn 1 người"
            
            # Trích xuất encoding
            face_encodings = face_recognition.face_encodings(image_array, face_locations)
            
            if len(face_encodings) == 0:
                return None, "Không thể trích xuất khuôn mặt"
            
            return face_encodings[0], None
            
        except Exception as e:
            return None, f"Lỗi xử lý ảnh: {str(e)}"
    
    # ===================================================================
    # ===== HÀM NÀY ĐÃ ĐƯỢC CẬP NHẬT ĐỂ LƯU FILE ẢNH =====
    # ===================================================================
    @staticmethod
    def register_face(user_id, image_data, photo_path=None):
        """
        Đăng ký khuôn mặt cho user.
        Đầu vào 'image_data' là dữ liệu bytes của ảnh.
        """
        
        # 1. Trích xuất vector (encoding) từ dữ liệu bytes
        encoding, error = FaceService.extract_face_encoding(image_data)
        
        if error:
            return None, error
        
        try:
            # 2. Lưu file ảnh vào thư mục /app/static/uploads
            
            # Tạo một tên file duy nhất (ví dụ: 1a2b3c4d.jpg)
            if not photo_path:
                filename = f"{uuid.uuid4().hex[:10]}.jpg"
                # Đảm bảo thư mục 'uploads' tồn tại
                upload_dir = os.path.join('app', 'static', 'uploads')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Đường dẫn đầy đủ để lưu file
                save_path = os.path.join(upload_dir, filename)
                
                # Đường dẫn tương đối để lưu vào DB (vd: uploads/1a2b3c4d.jpg)
                db_photo_path = os.path.join('uploads', filename)
            else:
                # Nếu có truyền tên file (trường hợp cũ), giữ nguyên
                save_path = os.path.join('app', 'static', 'uploads', photo_path)
                db_photo_path = os.path.join('uploads', photo_path)

            # Ghi dữ liệu bytes của ảnh ra file
            with open(save_path, 'wb') as f:
                f.write(image_data)
            
            print(f"✅ Đã lưu file ảnh tại: {save_path}")

            # 3. Kiểm tra user đã đăng ký khuôn mặt chưa (xóa cái cũ nếu có)
            existing = FaceData.query.filter_by(user_id=user_id).first()
            if existing:
                # Xóa file ảnh cũ (nếu có)
                if existing.photo_path:
                    old_path = os.path.join('app', 'static', existing.photo_path)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                db.session.delete(existing)
            
            # 4. Tạo record mới trong DB
            face_data = FaceData(user_id=user_id, photo_path=db_photo_path)
            face_data.set_encoding(encoding) # Lưu vector
            
            db.session.add(face_data)
            db.session.commit()
            
            print(f"✅ Đã lưu vector và đường dẫn ảnh vào DB cho User {user_id}")
            
            return face_data, None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Lỗi đăng ký: {str(e)}"
    # ===================================================================

    
    @staticmethod
    def recognize_face(image_data):
        """Nhận diện khuôn mặt (đầu vào là bytes)"""
        
        # 1. Trích xuất vector của ảnh đầu vào
        encoding, error = FaceService.extract_face_encoding(image_data)
        
        if error:
            return None, 0, error
        
        try:
            # 2. Lấy tất cả face encodings (vector) từ database
            all_faces = FaceData.query.all()
            
            if not all_faces:
                return None, 0, "Chưa có khuôn mặt nào được đăng ký"
            
            # 3. So sánh khuôn mặt
            stored_encodings = [f.get_encoding() for f in all_faces]
            distances = face_recognition.face_distance(stored_encodings, encoding)
            
            min_distance_idx = np.argmin(distances)
            min_distance = distances[min_distance_idx]
            
            # Tính confidence (1 - distance)
            confidence = max(0, 1 - min_distance) * 100
            
            if confidence < Config.FACE_CONFIDENCE_THRESHOLD * 100:
                return None, confidence, f"Confidence thấp: {confidence:.2f}%"
            
            face_data = all_faces[min_distance_idx]
            return face_data, confidence, None
            
        except Exception as e:
            return None, 0, f"Lỗi nhận diện: {str(e)}"