import os
from flask import Flask, render_template
from .models import db, Student
from .extensions import bcrypt, login_manager
from . import views

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates')
    )

    app.config['SECRET_KEY'] = 'su-safecampus-secret-key-change-in-prod'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cybersecurity.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = True

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        return Student.query.get(int(user_id))

    app.register_blueprint(views.main)
    app.register_blueprint(views.auth, url_prefix='/auth')
    app.register_blueprint(views.admin, url_prefix='/admin')

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    with app.app_context():
        db.create_all()

    return app
