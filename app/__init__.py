from flask import Flask
# Importing configuration class from the config.py file
from config import Config
# Importing Flask-Login to handle user log ins and outs
from flask_login import LoginManager
# Imports for database use
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm


# Database initialization
db = SQLAlchemy()
# migrate = Migrate(app, db)
login_helper = LoginManager()
login_helper.login_view = 'users_bp.login'

def create_app():
    app = Flask(__name__, template_folder='./templates', static_folder='./static')
    app.config.from_object(Config)

    db.init_app(app)
    login_helper.init_app(app)

    with app.app_context():
        from .main.routes import bp as main_bp
        from .users.routes import bp as users_bp

        db.create_all()

        app.register_blueprint(main_bp, url_prefix='/')
        app.register_blueprint(users_bp, url_prefix='/users')

    return app
