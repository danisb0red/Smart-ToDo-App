from datetime import datetime, timedelta, timezone
from flask import Blueprint,  jsonify, make_response, request
from models.user_model import User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from init import db


user_bp = Blueprint("user",__name__)

@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        firstName = data.get('firstName')
        lastName = data.get('lastName')
        email = data.get('email')
        password = data.get('password')
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'success': 'False','message': 'User already exits. Please Log in.'}), 400
        hashedPassword = generate_password_hash(password)
        newUser = User(first_name=firstName, last_name=lastName, email= email, password=hashedPassword)
        db.session.add(newUser)
        db.session.commit()
        return jsonify({'success': 'True','message': 'User added successfully.','data':newUser.toJSON()}),200
    return jsonify({'message' : 'Error'}),400

@user_bp.route('/login', methods=[ 'POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
            return jsonify({'success': 'False','message': 'Invalid email or password'}), 401
    from app import app
    token = jwt.encode({'id': user.id, 'exp': datetime.now(timezone.utc) + timedelta(hours=1)},app.config['SECRET_KEY'], algorithm="HS256")
    user.setLastLoggedin()
    response = make_response(jsonify({'success': 'True','message': 'User logged in successfully.','data':user.toJSON()}),200)
    response.set_cookie('jwt_token',token)
    return response