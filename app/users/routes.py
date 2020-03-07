from flask import Blueprint, jsonify, make_response, request, render_template, flash, redirect, url_for
from flask import current_app as app
from flask_qrcode import QRcode
from flask_login import login_user, login_required, logout_user, current_user
import constants
from werkzeug.security import generate_password_hash, check_password_hash
from app.users.register_form import RegisterForm
from app.users.edit_profile_form import EditProfileForm
from app.models import User, Recipes, Pantry
from app.users.two_factor import get_totp, generate_secret
from app import db

bp = Blueprint('users', __name__, template_folder='templates')
qrcode = QRcode(app)


@bp.route('/user/<username>')
@login_required
def user(username):
    # If user is found then the first appearance of the user is returned otherwise we get a 404 error if no match
    user = User.query.filter_by(username=username).first_or_404()
    # print(user.id)
    total_recipes = len(Recipes.query.filter_by(added_by=user.id).all())
     # print(len(total_recipes))
    total_pantry = len(Pantry.query.filter_by(owner=user.id).all())
    return render_template('user.html', user=user, total_recipes=total_recipes, total_pantry=total_pantry)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    payload = dict()
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
        user = User.query.filter_by(id=current_user.id).first()
        if user.two_factor == False:
            payload['twofa'] = False
        else:
            payload['twofa'] = True
    return render_template('edit_profile.html', title='Edit Profile', form=form, payload=payload)


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

        # Find the user
        user =  User.query.filter_by(username=username).first()

        if user:
            password_is_correct = check_password_hash(user.password, password)

            # Valid credentials are presented
            if password_is_correct:
                login_user(user)
                if user.two_factor == True:
                    return redirect(url_for('users.two_factor_login', user_id=(current_user.id)))
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


@bp.route('/<user_id>/2fa_setup', methods=constants.http_verbs)
@login_required
def two_factor_setup(user_id):
    payload = dict()
    if request.method == 'GET':
        user = User.query.filter_by(id=user_id).first()
        user_email = user.email_addr
        secret = generate_secret()
        user.secret = secret
        db.session.commit()
        totp_code = 'otpauth://totp/TheNeighborhoodCookbook:' + user_email + '?secret=' + secret + '&issuer=TheNeighborhoodCookbook'
        payload['qr'] = qrcode(totp_code)
        return render_template('two_factor_setup.html', payload=payload)
    if request.method == 'POST':
        entered_code = request.form.get('code')
        user = User.query.filter_by(id=user_id).first()
        user_secret = user.secret
        code = get_totp(user_secret)
        if code == entered_code:
            payload['success'] = True
            user.two_factor = True
            db.session.commit()
            return render_template('two_factor_setup.html', payload=payload)
        else:
            user = User.query.filter_by(id=user_id).first()
            user_email = user.email_addr
            secret = generate_secret()
            user.secret = secret
            db.session.commit()
            totp_code = 'otpauth://totp/TheNeighborhoodCookbook:' + user_email + '?secret=' + secret + '&issuer=TheNeighborhoodCookbook'
            payload['qr'] = qrcode(totp_code)
            payload['message'] = 'Incorrect code provided. Please add the new QR code to your Google Authenticator App and enter the 6-digit code within the 30 second lifetime.'
            return render_template('two_factor_setup.html', payload=payload)


@bp.route('/<user_id>/2fa', methods=constants.http_verbs)
@login_required
def two_factor_login(user_id):
    payload = dict()
    if request.method == 'GET':
        return render_template('two_factor_login.html', payload=payload)
    elif request.method == 'POST':
        payload = dict()
        entered_code = request.form.get('code')
        user = User.query.filter_by(id=user_id).first()
        user_secret = user.secret
        code = get_totp(user_secret)
        if code == entered_code:
            return redirect(url_for('main.index'))
        else:
            payload['message'] = 'Incorrect code provided. Please add the new QR code to your Google Authenticator App and enter the 6-digit code within the 30 second lifetime.'
            return render_template('two_factor_login.html', payload=payload)


@bp.route('/<user_id>/2fa_remove', methods=constants.http_verbs)
@login_required
def two_factor_remove(user_id):
    if request.method == 'GET':
        user = User.query.filter_by(id=user_id).first()
        user.two_factor = False
        db.session.commit()
        payload = dict()
        payload['twofa'] = False
        payload['message'] = 'Two-factor Authentication has been disabled.'
        form = EditProfileForm(current_user.username)
        form.username.data = current_user.username
        form.email.data = current_user.email_addr
        return render_template('edit_profile.html', form=form, payload=payload)


@bp.route('/recipes', methods=constants.http_verbs)
@login_required
def save_recipe():
    if request.method == 'POST':
        recipe_name = request.form.get('title')
        recipe_url = request.form.get('url')
        user_id = request.form.get('user')
        recipe_type = request.form.get('type')
        # Find the user
        user = User.query.filter_by(id=user_id).first()

        new_recipe = Recipes(recipe_name=recipe_name, source_url=recipe_url, added_by=user.id, type_recipe=recipe_type)
        # Add the new recipe to the db
        db.session.add(new_recipe)
        db.session.commit()

        print(recipe_name)
        print(recipe_url)
        print(f'Submitted user is {user_id} and user in db is {user.id}.')
        print('Printed from /users/recipes')
    return "Successful POST request"


@bp.route('/<user_id>/recipes', methods=constants.http_verbs)
@login_required
def get_recipes(user_id):
    if request.method == 'GET':
        # Find the user
        user = User.query.filter_by(id=user_id).first()
        recipes = Recipes.query.filter_by(added_by=user_id).all()
        return render_template('my_recipes.html', recipes=recipes)


@bp.route('/recipes/<recipe_id>', methods=constants.http_verbs)
@login_required
def delete_recipes(recipe_id):
    if request.method == 'DELETE':
        # Find the user
        user = User.query.filter_by(id=current_user.id).first()
        recipe = Recipes.query.filter_by(id=recipe_id).first()

        if recipe.added_by == user.id:
            db.session.delete(recipe)
            db.session.commit()
            return "Successful deletion."
        else:
            return "Unable to delete this recipe."


@bp.route('/logout', methods=constants.http_verbs)
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
