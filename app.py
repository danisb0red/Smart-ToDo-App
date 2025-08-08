from init import create_app

from models.task.task_model import Task
from routes.task.task_routes import scheduler
from routes.user.user_routes import user_bp
from routes.task.task_routes import task_bp

app = create_app()
#with app.app_context():
   # sendReminder()
app.register_blueprint(user_bp)
app.register_blueprint(task_bp)
if __name__ == "__main__":
    scheduler.start()
    app.run(debug = True)