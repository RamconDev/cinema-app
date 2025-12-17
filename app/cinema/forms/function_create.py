from flask_wtf import FlaskForm
from wtforms.fields import DateTimeLocalField, SelectField, StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class RegisterFunctionForm(FlaskForm):
    start_function = DateTimeLocalField("Date Time Start Function", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    auditorium = SelectField('Auditorium', coerce=int, validators=[DataRequired()])
    movie = SelectField('Movie', coerce=int, validators=[DataRequired()])

    submit = SubmitField("Register")