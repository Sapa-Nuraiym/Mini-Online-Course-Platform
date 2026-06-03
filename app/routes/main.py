from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/courses-page')
def courses_page():
    return render_template('courses.html')

@main_bp.route('/register-page')
def register_page():
    return render_template('register.html')

@main_bp.route('/login-page')
def login_page():
    return render_template('login.html')