from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectMultipleField, widgets, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ReservationsSeatsForm(FlaskForm):
    seats = SelectMultipleField(
        "Seats",
        coerce=int,  # convierte a int los IDs
        option_widget=widgets.CheckboxInput(),  # renderiza como checkboxes
        widget=widgets.ListWidget(prefix_label=False)  # lista de checkboxes
    )

    submit = SubmitField('Get Seats')