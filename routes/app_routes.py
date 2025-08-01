from flask import Blueprint, render_template

app_bp = Blueprint("app",__name__)


@app_bp.route('/')
def index():
    return render_template("home.html")

@app_bp.route('/about')
def about():
    return render_template("about.html")