import datetime
from flask import Blueprint,  jsonify, make_response, request

from models.db import db
from models.task.task_model import Task
from routes.user.user_utils import check_Token
from datetime import datetime, timedelta, timezone
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from init import mail


task_bp = Blueprint("task",__name__)
scheduler = BackgroundScheduler()

@task_bp.route('/create',methods= ['POST'])
def create():
     """ Create api for task. """
     try :
          data = request.get_json()
          title = data.get('title', None)
          description = data.get('description',"")
          date_string = data.get('dueAt',None)
          try:
               dueAt = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
               dueAt = dueAt.replace(tzinfo=timezone.utc)
          except:
                    return jsonify({'success': 'False','message': 'Incorrect DateTime format.'}), 400
          if dueAt < datetime.now(timezone.utc):
                    return jsonify({'success': 'False','message': 'Due time cannot be before current time.' }), 400
          token = request.cookies.get('jwt_token')
          current_user = check_Token(token)
          if current_user == None :
               return  jsonify({'success': 'False','message': 'Token is missing or invalid'}), 201
          user_id = current_user.id
          if title == None or dueAt == None :
                    return jsonify({'success': 'False','message': 'All fields are required.'}), 400
          if title == "" or dueAt == "" :
                    return jsonify({'success': 'False','message': 'Requied fields cannot be blank.'}), 400
          exsiting_task = Task.query.filter((Task.user_id == user_id) & (Task.title == title)).first()
          if exsiting_task:
               return jsonify({'success': 'False','message': 'Task with given title already exists.'}), 400
          newTask = Task(title=title,description=description,dueAt=dueAt,user_id=user_id)
          db.session.add(newTask)
          db.session.commit()
          reminder_time = dueAt - timedelta(minutes=10)
          user_mail = current_user.email
          scheduler.add_job(
               id=f"reminder_{title}_{user_id}",
               func= Task.sendReminder,
               trigger='date',
               run_date=reminder_time,
               args=[ title, dueAt, user_mail]
          )
          print("added job")
          scheduler.print_jobs()
          return jsonify({'success': True,'message': 'Task added successfully.','data':newTask.toJSON()}),200
     except Exception as e:
           return jsonify({'success': False,'message': str(e)}), 500


@task_bp.route('/view',methods= ['GET'])
def display_all_tasks():
     """ Reads all tasks for logged in user. """
     try:
          scheduler.print_jobs()
          print(datetime.now(timezone.utc))
          token = request.cookies.get('jwt_token')
          current_user = check_Token(token)
          if current_user == None :
               return  jsonify({'success': 'False','message': 'Token is missing or invalid'}), 201
          user_id = current_user.id
          tasks_list = Task.query.filter_by(user_id=user_id).all()
          taskinJSON =[]
          for temptask in tasks_list:
               taskinJSON.append(temptask.toJSON())
          return taskinJSON
     except Exception as e:
            return jsonify({'success': False,'message': str(e)}), 500

@task_bp.route('/update-task',methods=['PATCH'])
def update_task():
     """ Update api for task. """
     try:
          token = request.cookies.get('jwt_token')
          current_user = check_Token(token)
          if current_user == None :
               return  jsonify({'success': 'False','message': 'Token is missing or invalid'}), 401
          user_id = current_user.id
          data = request.get_json()
          title = data.get("title",None)
          if title == None or title == "":
               return jsonify({'success': 'False','message': 'Title needed to update a task.'}), 201
          new_title = data.get("new title", None)
          new_description = data.get("new description",None)
          target_task = Task.query.filter((Task.user_id == user_id) & (Task.title == title)).first()
          if new_title != "" and new_title != None :
               target_task.title = new_title
          if new_description != "" and new_description != None:
               target_task.description = new_description
          if new_title == "" and new_description == "":
               return jsonify({'success': 'False','message': 'No updated data provided'}), 201
          if new_title == None and new_description == None:
               return jsonify({'success': 'False','message': 'No updated data provided'}), 201
          target_task.set_Last_Updated()
          return jsonify({'success': 'True','message': 'Task was updated successfully.','data':target_task.toJSON()}), 201
     except Exception as e:
           return jsonify({'success': False,'message': str(e)}), 500


@task_bp.route("/delete-task",methods=["DELETE"])
def delete_task():
     """ Delete api for task. """
     try:
          token = request.cookies.get('jwt_token')
          current_user = check_Token(token)
          if current_user == None :
               return  jsonify({'success': 'False','message': 'Token is missing or invalid'}), 401
          user_id = current_user.id
          data = request.get_json()
          targ_title = data.get("title",None)
          if targ_title == None:
               return jsonify({'success': 'False','message': 'Title required to delete a task.'}),401
          target_task = Task.query.filter((Task.user_id == user_id) & (Task.title == targ_title)).first()
          if not target_task :
               return jsonify({'success': 'False','message': 'Task does not exist.'}), 401
          db.session.delete(target_task)
          db.session.commit()
          return jsonify({'success': 'True','message': 'Task was deleted.'}), 201
     except Exception as e:
            return jsonify({'success': False,'message': str(e)}), 500