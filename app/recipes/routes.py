from flask import Flask, Blueprint, jsonify, make_response, request, render_template, flash, redirect, url_for, json
from flask import current_app as app
from flask_login import login_user, login_required, logout_user, current_user
import constants
from werkzeug.security import generate_password_hash, check_password_hash
from app.users.register_form import RegisterForm
from app.users.edit_profile_form import EditProfileForm
from app.models import User
from app import db
from app.scraper.scraper import get_recipe, recipe_search
from app import celery
from app import create_app

bp = Blueprint('recipes', __name__, template_folder='templates')

@bp.route('/', methods=constants.http_verbs)
def find_recipes():
    if request.method == 'GET':
        return render_template('find_recipes.html')

@bp.route('/search/<ingredient>', methods=['GET'])
def recipe_search(ingredient):
    task = search_for_recipes.apply_async((ingredient,))
    return json.dumps({}), 202, {'Location': url_for('recipes.taskstatus', task_id=task.id)}

@bp.route('/status/<task_id>', methods=constants.http_verbs)
def taskstatus(task_id):
    task = search_for_recipes.AsyncResult(task_id)
    if task.state != 'FAILURE':
        if task.state == 'SUCCESS':
            response = {
                'state': task.state,
                'result': task.info
            }
        else:
            response = {
                'state': task.state,
                'status': 'Still working...'
            }
    else:
        response = {
                'state': task.state,
                'status': str(task.info)
            }
    return json.dumps(response)

@celery.task(bind=True, max_retries=1)
def search_for_recipes(self, ingredient):
    data = recipe_search(ingredient)
    recipe_dict = {'recipes': data}
    return json.dumps(recipe_dict)