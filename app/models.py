# Based on tutorial found here: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database

# File where data tables will be modeled
from app import db, login_helper
from flask_login import UserMixin
from datetime import datetime


# User account table
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True, nullable=False)
    email_addr = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(64))
    last_seen = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return '<User {}>'.format(self.username)


# User's saved recipes table
class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(120), index=True, nullable=False)
    source_url = db.Column(db.String(1028), nullable=False)
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Recipe {}>'.format(self.body)


# User's ingredients/pantry table
class Pantry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(256), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    units_used = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<Pantry {}>'.format(self.body)


# User loader function used to load a user with a given ID
@login_helper.user_loader
def load_user(id):
    return User.query.get(int(id))
