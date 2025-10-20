import sys
import os

# Thêm backend vào path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db # Chỉ giữ lại create_app và db
# Bỏ dòng này: from app.models import User, Station, FaceData 

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Tạo thư mục uploads
        os.makedirs('app/static/uploads', exist_ok=True)
        
        # CHÚ Ý: Lệnh db.create_all() cần các models được định nghĩa,
        # nhưng chúng ta đã import chúng ngầm trong app/__init__.py
        
        db.create_all()
        
        # Nếu muốn thêm dữ liệu mẫu, bạn phải import models ở đây
        from app.models import Station # Import Models cục bộ trong app_context
        if Station.query.count() == 0:
            stations = [
                Station(station_name='Bến Thành', line='Line 1'),
                Station(station_name='Suối Tiên', line='Line 1'),
                Station(station_name='Ngã Tư Sáng', line='Line 1'),
                Station(station_name='Cầu Giấy', line='Line 2'),
                Station(station_name='Hoan Kiếm', line='Line 2'),
                Station(station_name='Long Biên', line='Line 2'),
            ]
            db.session.add_all(stations)
            db.session.commit()
            print("✅ Đã tạo dữ liệu ga mẫu")
        
        print("🚀 Chạy server...")
        app.run(debug=True, host='0.0.0.0', port=5000)
