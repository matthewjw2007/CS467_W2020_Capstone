from flask import Flask, Blueprint, jsonify, make_response, request, render_template, flash, redirect, url_for
from flask import current_app as app
from flask_login import login_user, login_required, logout_user, current_user
import constants
from werkzeug.security import generate_password_hash, check_password_hash
from app.users.register_form import RegisterForm
from app.users.edit_profile_form import EditProfileForm
from app.models import User
from app import db
from app.scraper.scraper import recipe_search

bp = Blueprint('recipes', __name__, template_folder='templates')


@bp.route('find_recipes', methods=constants.http_verbs)
def find_recipes():
    return render_template('find_recipes.html')

@bp.route('/search', methods=constants.http_verbs)
def search_for_recipes():

    if request.args:

        ingredients = request.args.get('ingredients')

        payload = recipe_search(ingredients.split())

    return render_template('find_recipes.html', payload=payload)