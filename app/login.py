# from flask import Flask, Blueprint, jsonify, make_response, request, flash
# import constants
# from flask_wtf import FlaskForm
# from flask_login import login_user
# from werkzeug.security import check_password_hash
# from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
# from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
# from app.models import User
# from app import db

# # Define the blueprint for login
# bp = Blueprint('login', __name__, url_prefix='/login')


# # Login form class
# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember_me = BooleanField('Remember Me')
#     submit = SubmitField('Sign In')

# # Setup route for /login
# # methods variable defines accepted methods to this route
# # using full list of HTTP verbs from constants.py to allow
# # for error handling if an invalid verb is submitted to this route
# @bp.route('/login', methods=constants.http_verbs)
# # @bp.route('/index', methods=constants.http_verbs)
# def get_login():
#     # GET
#     if request.method == 'POST':

#         username = request.form.get('username')
#         password = request.form.get('password')
#         remember = True if request.form.get('remember') else False

#         # Fidn the user
#         user =  User.query.filter_by(username=username).first()
#         password_is_correct = check_password_hash(user.password, password)

#         # Valid credentials are presented
#         if user and password_is_correct:
#             flash('A user with this email address already exists.')
#             return redirect(url_for('main'))

#         # Invalid credentials presented
#         else:
#             login_user(user)
#             return redirect(url_for('user'))
        
#     # All other verbs
#     else:

#         # Make a response object with a JSON body
#         res = make_response(jsonify(error='Invalid HTTP method used for request'))
#         res.status_code = 405
#         return res