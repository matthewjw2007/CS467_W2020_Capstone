from flask import Flask, Blueprint, jsonify, make_response, request
import constants
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User

# Define the blueprint for login
bp = Blueprint('login', __name__, url_prefix='/login')


# Login form class
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# Setup route for /login
# methods variable defines accepted methods to this route
# using full list of HTTP verbs from constants.py to allow
# for error handling if an invalid verb is submitted to this route
@bp.route('/', methods=constants.http_verbs)
@bp.route('/index', methods=constants.http_verbs)
def get_login():
    # GET
    if request.method == 'GET':

        # Make a response object with a JSON body
        res = make_response(jsonify(content="This is the login page"))
        res.status_code = 200
        return res
        
    # All other verbs
    else:

        # Make a response object with a JSON body
        res = make_response(jsonify(error='Invalid HTTP method used for request'))
        res.status_code = 405
        return res