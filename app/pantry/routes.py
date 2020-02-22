from flask import Flask, Blueprint, jsonify, make_response, request, render_template, flash, redirect, url_for
from flask import current_app as app
from flask_login import login_user, login_required, logout_user, current_user
import constants
from werkzeug.security import generate_password_hash, check_password_hash
from app.recipes.search_form import SearchForm
from app.models import User, Pantry
from app import db
from app.scraper.scraper import recipe_search
from app.scraper.all_recipes import get_all_recipe

bp = Blueprint('pantry', __name__, template_folder='templates')


@bp.route('/', methods=constants.http_verbs)
@login_required
def view_pantry():
    if request.method == 'POST':
        payload = dict()
        pantry_items = list()
        print ('Printing form data now!')
        print (request.json)
        for items in request.json:
            pantry_items.append(items['value'])
            print (pantry_items)
        for item in pantry_items:
            new_item = Pantry(owner=current_user.id, name=item, quantity=1, units_used='ounces')
            db.session.add(new_item)
            db.session.commit()
        payload['message'] = 'Successfully added items!'
        return render_template('pantry_list.html', payload=payload)
    if request.method == 'GET':
        payload = dict()
        pantry_items = Pantry.query.filter_by(owner=current_user.id).all()
        if pantry_items:
            payload['pantry'] = pantry_items
        else:
            payload['message'] = "You don't have any items in your pantry. Would you like to add some?"

        return render_template('pantry_list.html', payload=payload)

@bp.route('/<item_id>', methods=constants.http_verbs)
@login_required
def delete_item(item_id):
    if request.method == 'DELETE':
        # Find the user
        user = User.query.filter_by(id=current_user.id).first()
        item = Pantry.query.filter_by(id=item_id).first()

        if item.owner == user.id:
            db.session.delete(item)
            db.session.commit()
            return "Successful deletion."
        else:
            return "Unable to delete this recipe."