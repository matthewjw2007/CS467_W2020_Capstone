from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    ingredients = StringField('Search for Recipes', validators=[DataRequired()], render_kw={'placeholder': 'Ingredient1, Ingredient2, Ingredient3, ...'})
    submit = SubmitField('Search')
