from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length

from app.models import User

class RegisterNewUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(4, 16, message='Between 4 to 16 characters')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password')
    role = SelectField('Role', coerce=int)
    submit = SubmitField('Register')

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_to_edit = user

    def validate_email(self, field):
        existing = User.query.filter_by(email=field.data).first()
        if existing:
            if self.user_to_edit:
                if existing.id == self.user_to_edit.id:
                    return
            raise ValueError('Email is already registered.')