from datetime import datetime, timedelta, timezone
from models.db import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    createdAt = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    dueAt = db.Column(db.DateTime, default=datetime.now(timezone.utc) + timedelta(hours=1))
    updatedAt = db.Column(db.DateTime, default=datetime.now(timezone.utc ))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title,description,dueAt,user_id):
        self.title = title
        self.description = description
        self.dueAt = dueAt
        self.user_id = user_id

    def set_Last_Updated(self):
        """Setter for updatedAt attribute of Task"""
        self.updatedAt = datetime.now(timezone.utc)
        db.session.commit()

    def toJSON(self):
        """To provide JSON representation of a Task object."""
        return {'title': self.title,'description':self.description,'createdAt': self.createdAt,'dueAt' : self.dueAt,'updatedAt' : self.updatedAt, 'user_id':self.user_id}