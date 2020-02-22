from flask import Flask, Blueprint, jsonify, make_response, request, render_template, flash, redirect, url_for
from flask import current_app as app
from flask_login import login_user, login_required, logout_user, current_user
import constants
from werkzeug.security import generate_password_hash, check_password_hash
from app.recipes.search_form import SearchForm
from app.models import User, Recipes
from app import db
from app.scraper.scraper import recipe_search
from app.scraper.all_recipes import get_recipe
from app.scraper.food_network import getRecipe

bp = Blueprint('recipes', __name__, template_folder='templates')


@bp.route('/search', methods=constants.http_verbs)
def find_recipes():
    form = SearchForm()
    payload = dict()
    websites = []
    if request.method == 'POST':
        if request.form.get('ingredients') != '':
            if request.form.get('allRecipes') is not None:
                websites.append('allrecipes')
            if request.form.get('foodNetwork') is not None:
                websites.append('foodnetwork')
            if request.form.get('allSites') is not None and request.form.get('allRecipes') is None and request.form.get('foodNetwork') is None:
                websites.append('allrecipes')
                websites.append('foodnetwork')
            ingredients = request.form.get('ingredients').split()
            ingredientList = list()
            for item in ingredients:
                if item[-1].isalpha() != True:
                    item = item[:-1]
                ingredientList.append(item)
            payload = recipe_search(ingredientList, websites)
        else:
            payload = {'error': 'Nothing was entered in the search bar.'}
    return render_template('find_recipes.html', form=form, payload=payload)


@bp.route('/view', methods=constants.http_verbs)
def view_recipe():
    recipeType = request.args.get('type')
    recipeUrl = request.args.get('url')
    if recipeType == 'allrecipes':
        recipe = get_recipe(recipeUrl)
    else:
        recipe = getRecipe(recipeUrl)
    return render_template('show_recipe.html', payload=recipe)
