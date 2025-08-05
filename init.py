from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.user.user_routes import user_bp
from models.user.user_model import User
from models.user.user_db import db
from dotenv import load_dotenv
import os
load_dotenv()

def create_app():
    """To initialize the app."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_API_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.register_blueprint(user_bp)
    with app.app_context():
        db.create_all()

    return app