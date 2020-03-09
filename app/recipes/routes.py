from flask import Blueprint, request, render_template, jsonify, current_app
from flask_login import login_required
import constants
from app.recipes.search_form import SearchForm
from app.scraper.scraper import recipe_search
from app.scraper.all_recipes import get_all_recipe
from app.scraper.food_network import get_foodnetwork
from app.scraper.simply_recipes import get_simply_recipe
from app.models import User, Recipes
from app import db
import rq
from rq.job import Job

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
            payload['results'] = recipe_search(ingredient_list, websites)
        else:
            payload = {'error': 'Nothing was entered in the search bar.'}
    return render_template('find_recipes.html', title='Search', form=form, payload=payload)


@bp.route('/search/<user_id>', methods=constants.http_verbs)
@login_required
def user_find_recipes(user_id):
    form = SearchForm()
    payload = dict()
    websites = []
    if request.method == 'POST':
        if request.form.get('ingredients') != '':
            jobs = current_app.task_queue.jobs
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
            search_string = request.form.get('ingredients')
            print (f"Search_string is: {search_string}")
            ingredients = request.form.get('ingredients').split()
            ingredient_list = list()
            for item in ingredients:
                if not item[-1].isalpha():
                    item = item[:-1]
                ingredient_list.append(item)
            user = User.query.filter_by(id=user_id).first()
            task = current_app.task_queue.enqueue(recipe_search, ingredient_list, websites, failure_ttl=60)
            assign_task(user, task.id, search_string)
            payload = {
                'task_id': task.id,
                'message': f'Task {task.id} has been added to the search queue.',
                'status': None
            }
        else:
            payload = {'error': 'Nothing was entered in the search bar.'}
        return render_template('find_recipes.html', title='Search', form=form, payload=payload)


@bp.route('/search/<user_id>/current_searches/<task_id>', methods=constants.http_verbs)
@login_required
def view_search_results(user_id, task_id):
    form = SearchForm()
    recipes = []
    task = Job.fetch(task_id, connection=current_app.redis)
    user = User.query.filter_by(id=user_id).first()
    saved_recipes = Recipes.query.filter_by(added_by=user.id).all()
    if len(saved_recipes) > 0:
        for recipe in saved_recipes:
            recipes.append(recipe.recipe_name)
    payload = dict()
    payload['results'] = task.result
    print (payload)
    return render_template('find_recipes.html', title='Results', form=form, saved_recipes=recipes, payload=payload)


@bp.route('search/<user_id>/jobs', methods=constants.http_verbs)
@login_required
def num_jobs(user_id):
    payload = dict()
    user = User.query.filter_by(id=user_id).first()
    update_tasks(user)
    payload['num_jobs'] = user.num_searches
    return jsonify(payload)


@bp.route('search/<user_id>/current_searches', methods=constants.http_verbs)
@login_required
def users_searches(user_id):
    if request.method == 'GET':
        payload = dict()
        user = User.query.filter_by(id=user_id).first()
        # get all current tasks
        payload = get_tasks(user)
        # return tasks
        return jsonify(payload)
        

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
    return render_template('show_recipe.html', title='Recipe Details', payload=recipe)


def assign_task(user, task_id, search_string):
    num_tasks = user.num_searches

    if num_tasks <= 4:
        if num_tasks == 0:
            user.search_id_1 = task_id
            user.search_string_1 = search_string

        elif num_tasks == 1:
            user.search_id_2 = task_id
            user.search_string_2 = search_string

        elif num_tasks == 2:
            user.search_id_3 = task_id
            user.search_string_3 = search_string

        elif num_tasks == 3:
            user.search_id_4 = task_id
            user.search_string_4 = search_string

        else:
            user.search_id_5 = task_id
            user.search_string_5 = search_string

        user.num_searches = num_tasks + 1
    else:
        user.search_id_1 = user.search_id_2
        user.search_string_1 = user.search_string_2
        user.search_id_2 = user.search_id_3
        user.search_string_2 = user.search_string_3
        user.search_id_3 = user.search_id_4
        user.search_string_3 = user.search_string_4
        user.search_id_4 = user.search_id_5
        user.search_string_4 = user.search_string_5
        user.search_id_5 = task_id
        user.search_string_5 = search_string
    db.session.commit()


def update_tasks(user):
    # Get current number of searches
    num_tasks = 0
    if user.search_id_1 is not None:
        num_tasks = num_tasks + 1
    if user.search_id_2 is not None:
        num_tasks = num_tasks + 1
    if user.search_id_3 is not None:
        num_tasks = num_tasks + 1
    if user.search_id_4 is not None:
        num_tasks = num_tasks + 1
    if user.search_id_5 is not None:
        num_tasks = num_tasks + 1

    # Clean up current searches
    if user.search_id_1 is not None:
        try:
            task = Job.fetch(user.search_id_1, connection=current_app.redis)
        except rq.exceptions.NoSuchJobError:
            user.search_id_1 = None
            user.search_string_1 = None
            num_tasks = num_tasks - 1
            db.session.commit()
    
    if user.search_id_2 is not None:
        try:
            task = Job.fetch(user.search_id_2, connection=current_app.redis)
        except rq.exceptions.NoSuchJobError:
            user.search_id_2 = None
            user.search_string_2 = None
            num_tasks = num_tasks - 1
            db.session.commit()

    if user.search_id_3 is not None:
        try:
            task = Job.fetch(user.search_id_3, connection=current_app.redis)
        except rq.exceptions.NoSuchJobError:
            user.search_id_3 = None
            user.search_string_3 = None
            num_tasks = num_tasks - 1
            db.session.commit()

    if user.search_id_4 is not None:
        try:
            task = Job.fetch(user.search_id_4, connection=current_app.redis)
        except rq.exceptions.NoSuchJobError:
            user.search_id_4 = None
            user.search_string_4 = None
            num_tasks = num_tasks - 1
            db.session.commit()

    if user.search_id_5 is not None:
        try:
            task = Job.fetch(user.search_id_5, connection=current_app.redis)
        except rq.exceptions.NoSuchJobError:
            user.search_id_5 = None
            user.search_string_5 = None
            num_tasks = num_tasks - 1
            db.session.commit()

    # update search queue
    user.num_searches = num_tasks
    db.session.commit()
    update_cascade(user)


def update_cascade(user):
    if user.num_searches == 1:
        while user.search_id_1 is None:
            if user.search_id_1 is None and user.search_id_2 is not None:
                user.search_id_1 = user.search_id_2
                user.search_string_1 = user.search_string_2
                user.search_id_2 = None
                user.search_string_2 = None
                db.session.commit()

            if user.search_id_2 is None and user.search_id_3 is not None:
                user.search_id_2 = user.search_id_3
                user.search_string_2 = user.search_string_3
                user.search_id_3 = None
                user.search_string_3 = None
                db.session.commit()

            if user.search_id_3 is None and user.search_id_4 is not None:
                user.search_id_3 = user.search_id_4
                user.search_string_3 = user.search_string_4
                user.search_id_4 = None
                user.search_string_4 = None
                db.session.commit()

            if user.search_id_4 is None and user.search_id_5 is not None:
                user.search_id_4 = user.search_id_5
                user.search_string_4 = user.search_string_5
                user.search_id_5 = None
                user.search_string_5 = None
                db.session.commit()

    elif user.num_searches == 2:
        while user.search_id_1 is None or user.search_id_2 is None:
            if user.search_id_1 is None and user.search_id_2 is not None:
                user.search_id_1 = user.search_id_2
                user.search_string_1 = user.search_string_2
                user.search_id_2 = None
                user.search_string_2 = None
                db.session.commit()

            if user.search_id_2 is None and user.search_id_3 is not None:
                user.search_id_2 = user.search_id_3
                user.search_string_2 = user.search_string_3
                user.search_id_3 = None
                user.search_string_3 = None
                db.session.commit()

            if user.search_id_3 is None and user.search_id_4 is not None:
                user.search_id_3 = user.search_id_4
                user.search_string_3 = user.search_string_4
                user.search_id_4 = None
                user.search_string_4 = None
                db.session.commit()

            if user.search_id_4 is None and user.search_id_5 is not None:
                user.search_id_4 = user.search_id_5
                user.search_string_4 = user.search_string_5
                user.search_id_5 = None
                user.search_string_5 = None
                db.session.commit()

    elif user.num_searches == 3:
        while user.search_id_1 is None or user.search_id_2 is None or user.search_id_3 is None:
            if user.search_id_1 is None and user.search_id_2 is not None:
                user.search_id_1 = user.search_id_2
                user.search_string_1 = user.search_string_2
                user.search_id_2 = None
                user.search_string_2 = None
                db.session.commit()

            if user.search_id_2 is None and user.search_id_3 is not None:
                user.search_id_2 = user.search_id_3
                user.search_string_2 = user.search_string_3
                user.search_id_3 = None
                user.search_string_3 = None
                db.session.commit()

            if user.search_id_3 is None and user.search_id_4 is not None:
                user.search_id_3 = user.search_id_4
                user.search_string_3 = user.search_string_4
                user.search_id_4 = None
                user.search_string_4 = None
                db.session.commit()

            if user.search_id_4 is None and user.search_id_5 is not None:
                user.search_id_4 = user.search_id_5
                user.search_string_4 = user.search_string_5
                user.search_id_5 = None
                user.search_string_5 = None
                db.session.commit()

    elif user.num_searches == 4:
        while user.search_id_1 is None or user.search_id_2 is None or user.search_id_3 is None or user.search_id_4 is None:
            if user.search_id_1 is None and user.search_id_2 is not None:
                user.search_id_1 = user.search_id_2
                user.search_string_1 = user.search_string_2
                user.search_id_2 = None
                user.search_string_2 = None
                db.session.commit()

            if user.search_id_2 is None and user.search_id_3 is not None:
                user.search_id_2 = user.search_id_3
                user.search_string_2 = user.search_string_3
                user.search_id_3 = None
                user.search_string_3 = None
                db.session.commit()

            if user.search_id_3 is None and user.search_id_4 is not None:
                user.search_id_3 = user.search_id_4
                user.search_string_3 = user.search_string_4
                user.search_id_4 = None
                user.search_string_4 = None
                db.session.commit()

            if user.search_id_4 is None and user.search_id_5 is not None:
                user.search_id_4 = user.search_id_5
                user.search_string_4 = user.search_string_5
                user.search_id_5 = None
                user.search_string_5 = None
                db.session.commit()


def get_tasks(user):
    payload = dict()
    task_arr = list()
    update_tasks(user)
    if user.search_id_1 is not None:
        message = dict()
        try:
            task = Job.fetch(user.search_id_1, connection=current_app.redis)
            message['status'] = task.get_status()
            message['task_id'] = user.search_id_1
            message['search_string'] = user.search_string_1
            if task.get_status() == 'failed':
                message['results'] = 'Job failed!'
            elif task.get_status() == 'finished':
                message['results'] = 'Job complete. Click to view results.'
            else:
                message['results'] = 'Job not finished...'
        except rq.exceptions.NoSuchJobError:
            user.search_id_1 = None
            user.search_string_1 = None
            db.session.commit()
            message['task_id'] = 'N/A'
            message['results'] = 'Something went wrong!'
        task_arr.append(message)

    if user.search_id_2 is not None:
        message = dict()
        try:
            task = Job.fetch(user.search_id_2, connection=current_app.redis)
            message['status'] = task.get_status()
            message['task_id'] = user.search_id_2
            message['search_string'] = user.search_string_2
            if task.get_status() == 'failed':
                message['results'] = 'Job failed!'
            elif task.get_status() == 'finished':
                message['results'] = 'Job complete. Click to view results.'
            else:
                message['results'] = 'Job not finished...'
        except rq.exceptions.NoSuchJobError:
            user.search_id_2 = None
            user.search_string_2 = None
            db.session.commit()
            message['task_id'] = 'N/A'
            message['results'] = 'Something went wrong!'
        task_arr.append(message)

    if user.search_id_3 is not None:
        message = dict()
        try:
            task = Job.fetch(user.search_id_3, connection=current_app.redis)
            message['status'] = task.get_status()
            message['task_id'] = user.search_id_3
            message['search_string'] = user.search_string_3
            if task.get_status() == 'failed':
                message['results'] = 'Job failed!'
            elif task.get_status() == 'finished':
                message['results'] = 'Job complete. Click to view results.'
            else:
                message['results'] = 'Job not finished...'
        except rq.exceptions.NoSuchJobError:
            user.search_id_3 = None
            user.search_string_3 = None
            db.session.commit()
            message['task_id'] = 'N/A'
            message['results'] = 'Something went wrong!'
        task_arr.append(message)

    if user.search_id_4 is not None:
        message = dict()
        try:
            task = Job.fetch(user.search_id_4, connection=current_app.redis)
            message['status'] = task.get_status()
            message['task_id'] = user.search_id_4
            message['search_string'] = user.search_string_4
            if task.get_status() == 'failed':
                message['results'] = 'Job failed!'
            elif task.get_status() == 'finished':
                message['results'] = 'Job complete. Click to view results.'
            else:
                message['results'] = 'Job not finished...'
        except rq.exceptions.NoSuchJobError:
            user.search_id_5 = None
            user.search_string_5 = None
            db.session.commit()
            message['task_id'] = 'N/A'
            message['results'] = 'Something went wrong!'
        task_arr.append(message)
    if user.search_id_5 is not None:
        message = dict()
        try:
            task = Job.fetch(user.search_id_5, connection=current_app.redis)
            message['status'] = task.get_status()
            message['task_id'] = user.search_id_5
            message['search_string'] = user.search_string_5
            if task.get_status() == 'failed':
                message['results'] = 'Job failed!'
            elif task.get_status() == 'finished':
                message['results'] = 'Job complete. Click to view results.'
            else:
                message['results'] = 'Job not finished...'
        except rq.exceptions.NoSuchJobError:
            user.search_id_5 = None
            user.search_string_5 = None
            db.session.commit()
            message['task_id'] = 'N/A'
            message['results'] = 'Something went wrong!'
        task_arr.append(message)
    payload['tasks'] = task_arr
    return payload
