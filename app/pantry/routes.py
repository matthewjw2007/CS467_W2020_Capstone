from flask import Flask, Blueprint, jsonify, make_response, request, render_template, flash, redirect, url_for
from flask import current_app as app
from flask_login import login_user, login_required, logout_user, current_user
import constants
from werkzeug.security import generate_password_hash, check_password_hash
from app.recipes.search_form import SearchForm
from app.models import User, Pantry
from app import db

bp = Blueprint('pantry', __name__, template_folder='templates')

@bp.route('/', methods=constants.http_verbs)
@login_required
def view_pantry():
    if request.method == 'POST':
        pantry_items = request.form.get('pantry_items')
        payload = pantry_items
        return render_template('pantry_list.html', payload=payload)
    if request.method == 'GET':
        payload = dict()
        pantry_items = Pantry.query.filter_by(owner=current_user.id).first()
        if pantry_items:
            payload['pantry'] = pantry_items
        else:
            payload['message'] = "You don't have any items in your pantry. Would you like to add some?"

        return render_template('pantry_list.html', payload=payload)
