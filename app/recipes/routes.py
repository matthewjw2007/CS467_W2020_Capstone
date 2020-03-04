from flask import Blueprint, request, render_template, jsonify
from flask_login import login_required, current_user
import constants
from app.recipes.search_form import SearchForm
from app.scraper.scraper import recipe_search
from app.scraper.all_recipes import get_all_recipe
from app.scraper.food_network import get_foodnetwork
from app.scraper.simply_recipes import get_simply_recipe
from app.models import User
from app import db, r, q
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
    return render_template('find_recipes.html', form=form, payload=payload)

@bp.route('/search/<user_id>', methods=constants.http_verbs)
@login_required
def user_find_recipes(user_id):
    form = SearchForm()
    payload = dict()
    websites = []
    if request.method == 'POST':
        if request.form.get('ingredients') != '':
            jobs = q.jobs
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
            print (f"Sreach_string is: {search_string}")
            ingredients = request.form.get('ingredients').split()
            ingredient_list = list()
            for item in ingredients:
                if not item[-1].isalpha():
                    item = item[:-1]
                ingredient_list.append(item)
            user = User.query.filter_by(id=user_id).first()
            task = q.enqueue(recipe_search, ingredient_list, websites, failure_ttl=60)
            assign_task(user, task.id, search_string)
            payload = {
                'task_id': task.id,
                'message': f'Task {task.id} has been added to the search queue.',
                'status': None
            }
        else:
            payload = {'error': 'Nothing was entered in the search bar.'}
        return render_template('find_recipes.html', form=form, payload=payload)

@bp.route('/search/<user_id>/current_searches/<task_id>', methods=constants.http_verbs)
@login_required
def view_search_results(user_id, task_id):
    form = SearchForm()
    task = Job.fetch(task_id, connection=r)
    user = User.query.filter_by(id=user_id).first()
    payload = dict()
    payload['results'] = task.result
    print (payload)
    return(render_template('find_recipes.html', form=form, payload=payload))

@bp.route('search/<user_id>/jobs', methods=constants.http_verbs)
@login_required
def num_jobs(user_id):
    payload = dict()
    user = User.query.filter_by(id=user_id).first()
    update_tasks(user)
    payload['num_jobs'] = user.num_searches
    print (payload)
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
    return render_template('show_recipe.html', payload=recipe)

def assign_task(user, task_id, search_string):
    num_tasks = user.num_searches
    #last_search = user.most_recent_search
    if num_tasks <= 4:
        if num_tasks == 0:
            user.search_id_1 = task_id
            user.search_string_1 = search_string
            print (f"Adding task: {task_id} to user.search_id_1")
            print (f"user.search_id_1 is now: {user.search_id_1}")
        elif num_tasks == 1:
            user.search_id_2 = task_id
            user.search_string_2 = search_string
            print (f"Adding task: {task_id} to user.search_id_2")
            print (f"user.search_id_2 is now: {user.search_id_2}")
        elif num_tasks == 2:
            user.search_id_3 = task_id
            user.search_string_3 = search_string
            print (f"Adding task: {task_id} to user.search_id_3")
            print (f"user.search_id_3 is now: {user.search_id_3}")
        elif num_tasks == 3:
            user.search_id_4 = task_id
            user.search_string_4 = search_string
            print (f"Adding task: {task_id} to user.search_id_4")
            print (f"user.search_id_4 is now: {user.search_id_4}")
        else:
            user.search_id_5 = task_id
            user.search_string_5 = search_string
            print (f"Adding task: {task_id} to user.search_id_5")
            print (f"user.search_id_5 is now: {user.search_id_5}")
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
    print("Running update_tasks")
    num_tasks = user.num_searches
    print(f"Num tasks is: {num_tasks}")
    # Clean up current searches
    print ("Printing search_id_1")
    print(f"search_id_1 is: {user.search_id_1}")
    print(f"search_string_1 is: {user.search_string_1}")
    if user.search_id_1 is not None:
        try:
            task = Job.fetch(user.search_id_1, connection=r)
            print (task)
        except rq.exceptions.NoSuchJobError:
        #if task is None:
            print("Exception for search 1 thrown")
            user.search_id_1 = None
            user.search_string_1 = None
            user.num_searches = num_tasks - 1
            db.session.commit()
    print ("Printing search_id_2")
    print(f"search_id_2 is: {user.search_id_2}")
    print(f"search_string_2 is: {user.search_string_2}")
    if user.search_id_2 is not None:
        try:
            task = Job.fetch(user.search_id_2, connection=r)
        except rq.exceptions.NoSuchJobError:
        #if task is None:
            print("Exception for search 2 thrown")
            user.search_id_2 = None
            user.search_string_2 = None
            user.num_searches = num_tasks - 1
            db.session.commit()
    print ("Printing search_id_3")
    print(f"search_id_3 is: {user.search_id_3}")
    print(f"search_string_3 is: {user.search_string_3}")
    if user.search_id_3 is not None:
        try:
            task = Job.fetch(user.search_id_3, connection=r)
        #if task is None:
        except rq.exceptions.NoSuchJobError:
            print("Exception for search 3 thrown")
            user.search_id_3 = None
            user.search_string_3 = None
            user.num_searches = num_tasks - 1
            db.session.commit()
    print ("Printing search_id_4")
    print(f"search_id_4 is: {user.search_id_4}")
    print(f"search_string_4 is: {user.search_string_4}")
    if user.search_id_4 is not None:
        try:
            task = Job.fetch(user.search_id_4, connection=r)
        except rq.exceptions.NoSuchJobError:
        #if task is None:
            print("Exception for search 4 thrown")
            user.search_id_4 = None
            user.search_string_4 = None
            user.num_searches = num_tasks - 1
            db.session.commit()
    print ("Printing search_id_5")
    print(f"search_id_5 is: {user.search_id_5}")
    print(f"search_string_5 is: {user.search_string_5}")
    if user.search_id_5 is not None:
        try:
            task = Job.fetch(user.search_id_5, connection=r)
        except rq.exceptions.NoSuchJobError:
        #if task is None:
            print("Exception for search 5 thrown")
            user.search_id_5 = None
            user.search_string_5 = None
            user.num_searches = num_tasks - 1
            db.session.commit()
    # update search queue
    update_cascade(user)

def update_cascade(user):
    if user.num_searches == 1:
        i = 1
        while user.search_id_1 is None:
            if i == 1:
                if user.search_id_1 is None and user.search_id_2 is not None:
                    user.search_id_1 = user.search_id_2
                    user.search_string_1 = user.search_string_2
                    user.search_id_2 = None
                    user.search_string_2 = None
                    db.session.commit()
                    i = i + 1
            elif i == 2:
                if user.search_id_2 is None and user.search_id_3 is not None:
                    user.search_id_2 = user.search_id_3
                    user.search_string_3 = user.search_string_3
                    user.search_id_3 = None
                    user.search_string_3 = None
                    db.session.commit()
                    i = i + 1
            elif i == 3:
                if user.search_id_3 is None and user.search_id_4 is not None:
                    user.search_id_3 = user.search_id_4
                    user.search_string_3 = user.search_string_4
                    user.search_id_4 = None
                    user.search_string_4 = None
                    db.session.commit()
                    i = i + 1
            elif i == 4:
                if user.search_id_4 is None and user.search_id_5 is not None:
                    user.search_id_4 = user.search_id_5
                    user.search_string_4 = user.search_string_5
                    user.search_id_5 = None
                    user.search_string_5 = None
                    db.session.commit()
                    i = i + 1
            else:
                i = 1
    elif user.num_searches == 2:
        i = 1
        while user.search_id_1 is None or user.search_id_2 is None:
            if i == 1:
                if user.search_id_1 is None and user.search_id_2 is not None:
                    user.search_id_1 = user.search_id_2
                    user.search_string_1 = user.search_string_2
                    user.search_id_2 = None
                    user.search_string_2 = None
                    db.session.commit()
                    i = i + 1
            elif i == 2:
                if user.search_id_2 is None and user.search_id_3 is not None:
                    user.search_id_2 = user.search_id_3
                    user.search_string_3 = user.search_string_3
                    user.search_id_3 = None
                    user.search_string_3 = None
                    db.session.commit()
                    i = i + 1
            elif i == 3:
                if user.search_id_3 is None and user.search_id_4 is not None:
                    user.search_id_3 = user.search_id_4
                    user.search_string_3 = user.search_string_4
                    user.search_id_4 = None
                    user.search_string_4 = None
                    db.session.commit()
                    i = i + 1
            elif i == 4:
                if user.search_id_4 is None and user.search_id_5 is not None:
                    user.search_id_4 = user.search_id_5
                    user.search_string_4 = user.search_string_5
                    user.search_id_5 = None
                    user.search_string_5 = None
                    db.session.commit()
                    i = i + 1
            else:
                i = 1
    elif user.num_searches == 3:
        i = 1
        while user.search_id_1 is None or user.search_id_2 is None or user.search_id_3 is None:
            if i == 1:
                if user.search_id_1 is None and user.search_id_2 is not None:
                    user.search_id_1 = user.search_id_2
                    user.search_string_1 = user.search_string_2
                    user.search_id_2 = None
                    user.search_string_2 = None
                    db.session.commit()
                    i = i + 1
            elif i == 2:
                if user.search_id_2 is None and user.search_id_3 is not None:
                    user.search_id_2 = user.search_id_3
                    user.search_string_3 = user.search_string_3
                    user.search_id_3 = None
                    user.search_string_3 = None
                    db.session.commit()
                    i = i + 1
            elif i == 3:
                if user.search_id_3 is None and user.search_id_4 is not None:
                    user.search_id_3 = user.search_id_4
                    user.search_string_3 = user.search_string_4
                    user.search_id_4 = None
                    user.search_string_4 = None
                    db.session.commit()
                    i = i + 1
            elif i == 4:
                if user.search_id_4 is None and user.search_id_5 is not None:
                    user.search_id_4 = user.search_id_5
                    user.search_string_4 = user.search_string_5
                    user.search_id_5 = None
                    user.search_string_5 = None
                    db.session.commit()
                    i = i + 1
            else:
                i = 1
    elif user.num_searches == 4:
        i = 1
        while user.search_id_1 is None or user.search_id_2 is None or user.search_id_3 is None or user.search_id_4 is None:
            if i == 1:
                if user.search_id_1 is None and user.search_id_2 is not None:
                    user.search_id_1 = user.search_id_2
                    user.search_string_1 = user.search_string_2
                    user.search_id_2 = None
                    user.search_string_2 = None
                    db.session.commit()
                    i = i + 1
            elif i == 2:
                if user.search_id_2 is None and user.search_id_3 is not None:
                    user.search_id_2 = user.search_id_3
                    user.search_string_3 = user.search_string_3
                    user.search_id_3 = None
                    user.search_string_3 = None
                    db.session.commit()
                    i = i + 1
            elif i == 3:
                if user.search_id_3 is None and user.search_id_4 is not None:
                    user.search_id_3 = user.search_id_4
                    user.search_string_3 = user.search_string_4
                    user.search_id_4 = None
                    user.search_string_4 = None
                    db.session.commit()
                    i = i + 1
            elif i == 4:
                if user.search_id_4 is None and user.search_id_5 is not None:
                    user.search_id_4 = user.search_id_5
                    user.search_string_4 = user.search_string_5
                    user.search_id_5 = None
                    user.search_string_5 = None
                    db.session.commit()
                    i = i + 1
            else:
                i = 1


def get_tasks(user):
    payload = dict()
    task_arr = list()
    update_tasks(user)
    if user.search_id_1 is not None:
        message = dict()
        try:
            task = Job.fetch(user.search_id_1, connection=r)
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
            task = Job.fetch(user.search_id_2, connection=r)
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
            task = Job.fetch(user.search_id_3, connection=r)
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
            task = Job.fetch(user.search_id_4, connection=r)
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
            task = Job.fetch(user.search_id_5, connection=r)
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