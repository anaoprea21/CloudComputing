from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class FoodForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    restaurant = StringField('Restaurant', validators=[DataRequired()])
    calories = IntegerField('Calories', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    submit = SubmitField('Add Food')

class ViewFoodForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('View Food')