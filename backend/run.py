import sys
import os

# Thêm backend vào path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Station, FaceData

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Tạo thư mục uploads
        os.makedirs('app/static/uploads', exist_ok=True)
        
        # Khởi tạo database
        db.create_all()
        
        # # Thêm dữ liệu mẫu nếu chưa có
        # if Station.query.count() == 0:
        #     stations = [
        #         Station(station_name='Bến Thành', line='Line 1'),
        #         Station(station_name='Suối Tiên', line='Line 1'),
        #         Station(station_name='Ngã Tư Sáng', line='Line 1'),
        #         Station(station_name='Cầu Giấy', line='Line 2'),
        #         Station(station_name='Hoan Kiếm', line='Line 2'),
        #         Station(station_name='Long Biên', line='Line 2'),
        #     ]
        #     db.session.add_all(stations)
        #     db.session.commit()
        #     print("✅ Đã tạo dữ liệu ga mẫu")
        
        print("🚀 Chạy server...")