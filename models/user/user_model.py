from models.user.user_db import db
from datetime import datetime, timezone

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(80))
    isAdmin = db.Column(db.Boolean, default = False)
    createdAt = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updatedAt = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    lastLogin = db.Column(db.DateTime, default=None)

    def __init__(self, first_name,last_name,email,password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        if self.first_name == "admin":
            self.isAdmin = True
        else :
            self.isAdmin = False

    def set_Last_Loggedin(self):
        """Setter for lastlogin attribute of User"""
        self.lastLogin = datetime.now(timezone.utc)
        db.session.commit()
    def set_Last_Updated(self):
        """Setter for updatedAt attribute of User"""
        self.updatedAt = datetime.now(timezone.utc)
        db.session.commit()

    def toJSON(self):
        """To provide JSON representation of a User object."""
        return {'first_name': self.first_name,'last_name':self.last_name,'email':self.email,'isAdmin': self.isAdmin,'createdAt': self.createdAt,'updatedAt' : self.updatedAt, 'lastLogin':self.lastLogin}
