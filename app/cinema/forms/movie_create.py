from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectMultipleField, widgets, SubmitField
from wtforms.validators import DataRequired, NumberRange

class RegisterMovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    release_year = IntegerField("Year", validators=[DataRequired(), NumberRange(min=1900, max=2100)])
    duration_minutes = IntegerField('Duration Minutes', validators=[DataRequired(), NumberRange(min=0, max=500)])
    poster_url = StringField('poster', validators=[])
    options = SelectMultipleField(
        "Genres",
        coerce=int,  # convierte a int los IDs
        option_widget=widgets.CheckboxInput(),  # renderiza como checkboxes
        widget=widgets.ListWidget(prefix_label=False)  # lista de checkboxes
    )

    submit = SubmitField('Register')