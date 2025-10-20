from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    with app.app_context():
        # Import models
        from app.models import user, face_data, ticket, station, entry_log
        
        # Create tables
        db.create_all()
        
        # Register blueprints
        from app.routes import auth_routes, face_routes, ticket_routes
        app.register_blueprint(auth_routes.bp)
        app.register_blueprint(face_routes.bp)
        app.register_blueprint(ticket_routes.bp)
    
    return app