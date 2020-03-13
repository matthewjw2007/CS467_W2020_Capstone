# Based on tutorial found here: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database

# File where data tables will be modeled
from app import db, login_helper
from flask_login import UserMixin
from datetime import datetime


# User account table
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True, nullable=False)
    email_addr = db.Column(db.String(128), index=True, unique=True, nullable=False)
    password = db.Column(db.String(256))
    last_seen = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    two_factor = db.Column(db.Boolean, default=False)
    secret = db.Column(db.String(128))
    num_searches = db.Column(db.Integer, default=0)
    most_recent_search = db.Column(db.Integer, default=0)
    search_id_1 = db.Column(db.String(128))
    search_string_1 = db.Column(db.String(280))
    search_id_2 = db.Column(db.String(128))
    search_string_2 = db.Column(db.String(280))
    search_id_3 = db.Column(db.String(128))
    search_string_3 = db.Column(db.String(280))
    search_id_4 = db.Column(db.String(128))
    search_string_4 = db.Column(db.String(280))
    search_id_5 = db.Column(db.String(128))
    search_string_5 = db.Column(db.String(280))

    def __repr__(self):
        return '<User {}>'.format(self.username)


# User's saved recipes table
class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(120), index=True, nullable=False)
    source_url = db.Column(db.String(1028), nullable=False)
    type_recipe = db.Column(db.String(120))
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Recipe {self.id}, {self.recipe_name}, {self.source_url}, {self.added_by}, {self.type_recipe}'


# User's ingredients/pantry table
class Pantry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'Pantry {self.id}, {self.owner}, {self.name}, {self.quantity}, {self.units_used}'


# User loader function used to load a user with a given ID
@login_helper.user_loader
def load_user(id):
    return User.query.get(int(id))
