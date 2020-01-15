from app import app
from flask import render_template
from flask_login import current_user, login_user, logout_user, login_required
from app.login import LoginForm


@app.route('/')
@app.route('/index')
def index():
    form = LoginForm()
    return render_template('home.html', title='Home', form=form)


@app.route('/my_pantry')
def my_pantry():
    return render_template('my_pantry.html', title='My Pantry')
