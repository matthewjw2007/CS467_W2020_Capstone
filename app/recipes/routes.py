from flask import Flask, Blueprint, jsonify, make_response, request, render_template, flash, redirect, url_for
from flask import current_app as app
from flask_login import login_user, login_required, logout_user, current_user
import constants
from werkzeug.security import generate_password_hash, check_password_hash
from app.recipes.search_form import SearchForm
from app.models import User
from app import db
from app.scraper.scraper import recipe_search

bp = Blueprint('recipes', __name__, template_folder='templates')


@bp.route('find_recipes', methods=constants.http_verbs)
def find_recipes():
    form = SearchForm()
    if form.validate_on_submit():
        print('hello')
    return render_template('find_recipes.html', form=form)


@bp.route('/search', methods=constants.http_verbs)
def search_for_recipes():

    if request.args.get('ingredients') != '':

        ingredients = request.args.get('ingredients')

        payload = recipe_search(ingredients.split())

    else:

        payload = {'error': 'Nothing was entered in the search bar.'}

    return render_template('find_recipes.html', payload=payload)