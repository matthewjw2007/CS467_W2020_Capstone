from flask import Blueprint, make_response, request, render_template
from flask_login import login_required, current_user
import constants
from app.models import User, Pantry
from app import db

bp = Blueprint('pantry', __name__, template_folder='templates')


@bp.route('/', methods=constants.http_verbs)
@login_required
def view_pantry():
    user = User.query.filter_by(id=current_user.id).first()
    if request.method == 'POST':
        payload = dict()
        pantry_items = list()
        for items in request.json:
            pantry_items.append(items['value'])
        for item in pantry_items:
            new_item = Pantry(owner=current_user.id, name=item)
            db.session.add(new_item)
            db.session.commit()
        res = make_response()
        return '', 200
    if request.method == 'GET':
        payload = dict()
        pantry_items = Pantry.query.filter_by(owner=current_user.id).all()
        if pantry_items:
            payload['pantry'] = pantry_items
        else:
            payload['message'] = "You don't have any items in your pantry. Would you like to add some?"
        return render_template('pantry_list.html', title='My Pantry', user=user, payload=payload)


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
