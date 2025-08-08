from datetime import datetime, timedelta, timezone
import os
from flask_mail import Message
from models.db import db
from flask_mail import Mail, Message
from init import mail, app


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

    @staticmethod
    def sendReminder(title, dueAt, targmail):
        """Mails a reminder for tasks due in 10 minutes."""
        with app.app_context():
            msg = Message(
                    'Task Reminder',
                    sender = os.getenv("MAIL"),
                    recipients = [targmail]
                )
            msg_body = f"Reminder: Your task '{title}' is due in 10 minutes."
            msg.body = msg_body
            mail.send(msg)
            print("reminder sent.")

        '''''
        tasks = Task.query.all()
        for task in tasks:
            date = task.dueAt
            date = date.replace(tzinfo=timezone.utc)
            if (date - datetime.now(timezone.utc))  < timedelta(minutes=10):
                user_id = task.user_id
                targ_user = User.query.filter_by(id = user_id).first()
                targmail = targ_user.email
                msg = Message(
                'Task Reminder',
                sender = os.getenv("MAIL"),
                recipients = [targmail]
               )
                time_diff = date - datetime.now(timezone.utc)
                minutes_diff = int(time_diff.total_seconds() // 60)
                if time_diff.total_seconds() > 0:
                    if minutes_diff == 0:
                        msg_body = f"Reminder: Your task '{task.title}' is due right now."
                    else:
                        msg_body = f"Reminder: Your task '{task.title}' is due in {minutes_diff} minutes."
                else:
                    minutes_diff = abs(minutes_diff)
                    msg_body = f" Your task '{task.title}' was due {minutes_diff} minutes ago."

                msg.body = msg_body
                mail.send(msg)
                print(targmail)
            else:
                 print("good")
   '''