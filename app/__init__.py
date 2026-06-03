from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'

    db.init_app(app)

    with app.app_context():
        from app import models
        db.create_all()

        from app.routes.courses import courses_bp
        from app.routes.auth import auth_bp
        app.register_blueprint(courses_bp, url_prefix='/api')
        app.register_blueprint(auth_bp, url_prefix='/api')

    return app