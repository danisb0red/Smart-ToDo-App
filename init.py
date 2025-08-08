from datetime import datetime, timedelta, timezone
from flask import Flask
from models.db import db
from dotenv import load_dotenv
from flask_mail import Mail, Message
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import os
load_dotenv()
mail = Mail()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_API_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv("MAIL")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASS")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['SCHEDULER_API_ENABLED'] = True



def create_app():
    """To initialize the app."""
    db.init_app(app)
    mail.init_app(app)
    ''''
    app.register_blueprint(user_bp)
    app.register_blueprint(task_bp)
   '''

    with app.app_context():
        db.create_all()
    return app


