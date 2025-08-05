from datetime import datetime, timedelta, timezone
from flask import Blueprint,  jsonify, make_response, request
from models.user.user_model import User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from  models.user.user_db import db
from flask import current_app
import re
from routes.user.user_utils import check_Token, is_Admin
from dotenv import load_dotenv
import os

load_dotenv()
user_bp = Blueprint("user",__name__)

@user_bp.route('/signup', methods=['POST'])
def signup():
    """ Signup api for user """
    if request.method == 'POST':
        data = request.get_json()
        firstName = data.get('firstName', None)
        lastName = data.get('lastName',None)
        email = data.get('email',None)
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(regex, email):
          return jsonify({'success': 'False','message': 'Please enter correct email'}), 400
        else:
         password = data.get('password',None)
         if password.__len__() <6 :
              return jsonify({'success': 'False','message': 'Password should be atleast 6 characters long.'}), 400
         if firstName == None or lastName == None or email == None or password == None:
              return jsonify({'success': 'False','message': 'All fields are required.'}), 400
         if firstName == "" or lastName == "" or email == "" or password == "":
              return jsonify({'success': 'False','message': 'Requied fields cannot be blank.'}), 400
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
    """ Login api for user """
    data = request.get_json()
    email = data.get('email',None)
    password = data.get('password',None)
    if  email == None or password == None:
              return jsonify({'success': 'False','message': 'All fields are requied.'}), 400
    if  email == "" or password == "":
              return jsonify({'success': 'False','message': 'Requied fields cannot be blank.'}), 400
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
            return jsonify({'success': 'False','message': 'Invalid email or password'}), 401
   
    token = jwt.encode({'email': user.email, 'exp': datetime.now(timezone.utc) + timedelta(hours=1)},current_app.config['SECRET_KEY'], algorithm=os.getenv("JWT_ALGO"))
    user.set_Last_Loggedin()
    response = make_response(jsonify({'success': 'True','message': 'User logged in successfully.','data':user.toJSON()}),200)
    response.set_cookie('jwt_token',token)
    return response

@user_bp.route('/delete',methods = ['DELETE'])
def delete():
     """ Delete api for user """
     token = request.cookies.get('jwt_token')
     current_user = check_Token(token)
     if current_user == None :
          return  jsonify({'success': 'False','message': 'Token is missing or invalid'}), 201
     if not is_Admin(current_user):
          return jsonify({'success': 'False','message': 'Only admins can delete users.'}), 401
     data = request.get_json()
     email = data.get('target_email')
     regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
     if not re.match(regex, email):
         return jsonify({'success': 'False','message': 'Please enter correct email'}), 400
     user = User.query.filter_by(email=email).first()
     if user.email == current_user.email:
          return jsonify({'success': 'False','message':  'Cannot delete your own account.'}), 401
     if not user :
            return jsonify({'success': 'False','message': 'User does not exist.'}), 401
     db.session.delete(user)
     db.session.commit()
     return jsonify({'success': 'True','message': 'User was deleted.'}), 201



@user_bp.route('/update',methods = ['PATCH'])
def update():
     """ Update api for user """
     token = request.cookies.get('jwt_token')
     current_user = check_Token(token)
     if current_user == None :
          return  jsonify({'success': 'False','message': 'Token is missing or invalid'}), 201
     data = request.get_json()
     new_email = data.get('email',None)
     new_pass = data.get('password',None)
     if new_email != "" and new_email != None :
      current_user.email = new_email
     if new_pass != "" and new_pass != None:
        current_user.password = generate_password_hash(new_pass)
     if new_pass == "" and new_email == "":
          return jsonify({'success': 'False','message': 'No updated data provided'}), 201
     if new_pass == None and new_email == None:
          return jsonify({'success': 'False','message': 'No updated data provided'}), 201
     current_user.set_Last_Updated()
     return jsonify({'success': 'True','message': 'User was updated successfully.','data':current_user.toJSON()}), 201