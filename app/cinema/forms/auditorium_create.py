from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class RegisterAuditoriumForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    rows = IntegerField('Total rows', validators=[DataRequired(), NumberRange(min=5, max=15, message='Rows must be between 5 and 15.')])
    seats_per_row = IntegerField('Seats per Row', validators=[DataRequired(), NumberRange(min=8, message='Minimum 8 seats per row.')])
    submit = SubmitField('Register')