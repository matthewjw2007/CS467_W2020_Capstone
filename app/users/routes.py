from flask import Flask, Blueprint, jsonify, make_response, request, render_template, flash, redirect, url_for
from flask import current_app as app
from flask_login import login_user, login_required, logout_user, current_user
import constants
from werkzeug.security import generate_password_hash, check_password_hash
from app.users.register_form import RegisterForm
from app.users.edit_profile_form import EditProfileForm
from app.models import User
from app import db

bp = Blueprint('users', __name__, template_folder='templates')


@bp.route('/user/<username>')
@login_required
def user(username):
    # If user is found then the first appearance of the user is returned otherwise we get a 404 error if no match
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email_addr = form.email.data
        db.session.commit()
        flash('Profile updated')
        return redirect(url_for('users.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email_addr
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@bp.route('/delete_profile', methods=constants.http_verbs)
@login_required
def delete_profile():
    user = User.query.filter_by(username=current_user.username).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'GET':

        form = RegisterForm()
        return render_template('register.html', title='Register', form=form)

    if request.method == 'POST':

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check that the new user isn't already registered
        user = User.query.filter_by(email_addr=email).first()
        if user:
            flash('A user with this email address already exists.')
            return redirect(url_for('main.index'))

        else:
            # Create the new user object using the PBKDF2 with SHA-256 hashing standard with 10,000 iterations and a salt length of 128 bytes
            new_user = User(username=username, email_addr=email, password=generate_password_hash(password, method='pbkdf2:sha256:10000', salt_length=128))

            # Add the new user to the db
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('main.index'))
        
    # All other verbs
    else:
        # Make a response object with a JSON body
        res = make_response(jsonify(error='Invalid HTTP method used for request'))
        res.status_code = 405
        return res
        

# Setup route for /login
# methods variable defines accepted methods to this route
# using full list of HTTP verbs from constants.py to allow
# for error handling if an invalid verb is submitted to this route
@bp.route('/login', methods=constants.http_verbs)
# @bp.route('/index', methods=constants.http_verbs)
def login():
    # GET
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        # Fidn the user
        user =  User.query.filter_by(username=username).first()

        if user:
            password_is_correct = check_password_hash(user.password, password)

            # Valid credentials are presented
            if password_is_correct:
                login_user(user)
                return redirect(url_for('main.index'))
            
            else:
                flash('Incorrect username and/or password entered. Try again.')
                return redirect(url_for('main.index'))

        # Invalid credentials presented
        else:
            flash('Incorrect username and/or password entered. Try again.')
            return redirect(url_for('main.index'))
        
    # All other verbs
    else:

        # Make a response object with a JSON body
        res = make_response(jsonify(error='Invalid HTTP method used for request'))
        res.status_code = 405
        return res


@bp.route('/recipes', methods=constants.http_verbs)
def save_recipe():
    if request.method == 'POST':
        recipe_name = request.form.get('recipe-title')
        recipe_url = request.form.get('recipe-URL')

        print(recipe_name)
        print(recipe_url)
    return redirect(url_for('main.index'))


@bp.route('/logout', methods=constants.http_verbs)
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
