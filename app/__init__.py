from flask import Flask
# Importing configuration class from the config.py file
from config import Config
# Importing Flask-Login to handle user log ins and outs
from flask_login import LoginManager
# Imports for database use
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from redis import Redis
import rq

# Database initialization
db = SQLAlchemy()
login_helper = LoginManager()
# login_helper.login_view = 'users_bp.login'
# # Redis / rq intialization
# r = redis.Redis()
# q = Queue(connection=r)

def create_app():
    app = Flask(__name__, template_folder='./templates', static_folder='./static')
    app.config.from_object(Config)
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue(connection=app.redis)
    migrate = Migrate(app, db)
    db.init_app(app)
    login_helper.init_app(app)

    with app.app_context():
        from .main.routes import bp as main_bp
        from .users.routes import bp as users_bp
        from .recipes.routes import bp as recipes_bp
        from .pantry.routes import bp as pantry_bp

        login_helper.login_view = 'users.login'
        db.create_all()

        app.register_blueprint(main_bp, url_prefix='/')
        app.register_blueprint(users_bp, url_prefix='/users')
        app.register_blueprint(recipes_bp, url_prefix='/recipes')
        app.register_blueprint(pantry_bp, url_prefix='/pantry')

    return app
