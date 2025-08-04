from flask import Flask
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    from routes.user_routes import user_bp
    app.register_blueprint(user_bp)
    with app.app_context():
        from models.user_model import User
        db.create_all()

    return app