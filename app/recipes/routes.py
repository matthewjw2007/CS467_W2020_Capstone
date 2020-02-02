from flask import Flask, Blueprint, jsonify, make_response, request, render_template, flash, redirect, url_for
from flask import current_app as app
from flask_login import login_user, login_required, logout_user, current_user
import constants
from werkzeug.security import generate_password_hash, check_password_hash
from app.users.register_form import RegisterForm
from app.users.edit_profile_form import EditProfileForm
from app.models import User
from app import db
from app import r
from app import q
from app.scraper.scraper import recipe_search
from rq.job import Job

bp = Blueprint('recipes', __name__, template_folder='templates')


@bp.route('/', methods=constants.http_verbs)
def find_recipes():
    return render_template('find_recipes.html')

@bp.route('/search', methods=constants.http_verbs)
def search_for_recipes():

    jobs = q.jobs

    message = None

    if request.args:

        ingredient = request.args.get('ingredients')

        task = q.enqueue(recipe_search, ingredient)

        jobs = q.jobs

        q_len = len(q)

        payload = {
            'task_id': task.id,
            'results': f'Task {task.id} added to queue.',
            'status': None
        }

    return render_template('find_recipes.html', payload=payload)

@bp.route('/search/<task_id>', methods=constants.http_verbs)
def task_update(task_id):

    task = Job.fetch(task_id, connection=r)

    message = dict()

    message['task_id'] = task_id
    message['status'] = task.get_status()

    if task:
        if task.get_status() == 'failed':
            message['results'] = 'Job failed!'
        elif task.get_status() == 'finished':
            message['results'] = str(task.result)
        else:
            message['results'] = 'Job not finished...'

    else:
        message['results'] = 'Something went wrong!'

    return jsonify(message)
