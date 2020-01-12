# File where data tables will be modeled
from app import db, login_helper
from flask_login import UserMixin


# User table
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)

# User loader function used to load a user with a given ID
@login_helper.user_loader
def load_user(id):
    return User.query.get(int(id))