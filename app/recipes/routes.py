from flask import Blueprint, request, render_template
import constants
from app.recipes.search_form import SearchForm
from app.scraper.scraper import recipe_search
from app.scraper.all_recipes import get_all_recipe
from app.scraper.food_network import get_foodnetwork
from app.scraper.simply_recipes import get_simply_recipe

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
            if request.form.get('simplyRecipes') is not None:
                websites.append('simplyRecipes')
            if request.form.get('allSites') is not None and request.form.get('allRecipes') is None and request.form.get(
                    'foodNetwork') is None and request.form.get('simplyRecipes') is None:
                websites.append('allrecipes')
                websites.append('foodnetwork')
                websites.append('simplyRecipes')
            ingredients = request.form.get('ingredients').split()
            ingredient_list = list()
            for item in ingredients:
                if not item[-1].isalpha():
                    item = item[:-1]
                ingredient_list.append(item)
            payload = recipe_search(ingredient_list, websites)
        else:
            payload = {'error': 'Nothing was entered in the search bar.'}
    return render_template('find_recipes.html', form=form, payload=payload)


@bp.route('/view', methods=constants.http_verbs)
def view_recipe():
    recipe_type = request.args.get('type')
    recipe_url = request.args.get('url')
    if recipe_type == 'allrecipes':
        recipe = get_all_recipe(recipe_url)
    elif recipe_type == 'food_network':
        recipe = get_foodnetwork(recipe_url)
    else:
        recipe = get_simply_recipe(recipe_url)
    return render_template('show_recipe.html', payload=recipe)
