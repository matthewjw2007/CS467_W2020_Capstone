from flask import Flask, Blueprint, jsonify, make_response, request, render_template
from flask import current_app as app
import constants
from werkzeug.security import generate_password_hash
from app.users.login_form import LoginForm

bp = Blueprint('main', __name__, template_folder='templates')

@bp.route('')
def index():
    form = LoginForm()
    return render_template('home.html', title='Home', form=form)