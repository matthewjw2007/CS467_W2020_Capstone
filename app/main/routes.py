from flask import Blueprint, render_template
from app.users.login_form import LoginForm

bp = Blueprint('main', __name__, template_folder='templates')


@bp.route('')
@bp.route('/index')
def index():
    form = LoginForm()
    return render_template('home.html', title='Home', form=form)
