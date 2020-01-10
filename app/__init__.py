from flask import Flask
# Importing configuration class from the config.py file
from config import Config


app = Flask(__name__, template_folder='./templates', static_folder='./static')
app.config.from_object(Config)

# Import BP files
from app import users, pantry, recipes, login, register
# Register the blueprints for different routes
app.register_blueprint(login.bp)    # /login
app.register_blueprint(pantry.bp)   # /pantry
app.register_blueprint(recipes.bp)  # /recipes
app.register_blueprint(register.bp) # /register
app.register_blueprint(users.bp)    # /users

from app import routes, models
