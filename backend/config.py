import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Ví dụ cho MySQL
    SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL', 
    'mysql+pymysql://root:04012005@localhost/metro_db'
)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Upload settings
    UPLOAD_FOLDER = 'backend/app/static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Face recognition
    FACE_CONFIDENCE_THRESHOLD = 0.6
    
    # Pricing
    BASE_FARE = {
        1: 7000,    # 1 ga
        2: 9000,    # 2 ga
        3: 10000,   # 3+ ga
    }
    
    # Flask app settings
    JSON_AS_ASCII = False
    JSONIFY_PRETTYPRINT_REGULAR = True