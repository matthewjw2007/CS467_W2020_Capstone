from app import app
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', title='Home')


@app.route('/my_pantry')
def my_pantry():
    return render_template('my_pantry.html', title='My Pantry')
