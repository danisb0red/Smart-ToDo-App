from flask import current_app, jsonify
import jwt
from models.user.user_model import User


def check_Token(token):
     """ To check if token is valid. """
     if not token:
            return None
     try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(email=data['email']).first()
            return current_user
     except:
            return None

def is_Admin(current_user):
     """To check if the provided user is an admin."""
     isAdmin = current_user.isAdmin
     if (isAdmin != True):
          return False
     else:
           return True