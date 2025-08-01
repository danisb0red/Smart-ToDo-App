from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.app_routes import app_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(app_bp)
if __name__ == "__main__":
    app.run(debug = True)