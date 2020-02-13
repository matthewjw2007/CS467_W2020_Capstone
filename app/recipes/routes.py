from flask import Flask, Blueprint, jsonify, make_response, request, render_template, flash, redirect, url_for
from flask import current_app as app
from flask_login import login_user, login_required, logout_user, current_user
import constants
from werkzeug.security import generate_password_hash, check_password_hash
from app.recipes.search_form import SearchForm
from app.models import User, Recipes
from app import db
from app.scraper.scraper import recipe_search, get_recipe

bp = Blueprint('recipes', __name__, template_folder='templates')


@bp.route('/search', methods=constants.http_verbs)
def find_recipes():
    form = SearchForm()
    payload = dict()
    if request.method == 'POST':
        if request.form.get('ingredients') != '':
            ingredients = request.form.get('ingredients').split()
            ingredientList = list()
            for item in ingredients:
                if item[-1].isalpha() != True:
                    item = item[:-1]
                ingredientList.append(item)
            payload = recipe_search(ingredientList)
        else:
            payload = {'error': 'Nothing was entered in the search bar.'}
    return render_template('find_recipes.html', form=form, payload=payload)

@bp.route('/view', methods=constants.http_verbs)
def view_recipe():
    payload = dict()
    recipeUrl = request.args.get('url')
    recipe = get_recipe(recipeUrl)
    return render_template('show_recipe.html', payload=recipe)
