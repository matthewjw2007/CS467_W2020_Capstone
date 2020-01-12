# File where data tables will be modeled
from app import db, login_helper
from flask_login import UserMixin
from datetime import datetime


# User account table
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email_addr = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


# User's saved recipes table
class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(120), index=True, nullable=False)


# User's ingredients/pantry table
class UserPantry(db.Model):
    id = db.Column(db.Integer, primary_key=True)


# User loader function used to load a user with a given ID
@login_helper.user_loader
def load_user(id):
    return User.query.get(int(id))