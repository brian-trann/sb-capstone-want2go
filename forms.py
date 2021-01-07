from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Email, Length

class UserAddForm(FlaskForm):
    """Form for adding users."""
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('E-mail', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])

class LoginForm(FlaskForm):
    """Login form."""

    email = StringField('E-mail', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])

# Will need to think about making a form for the zipcode input
class SearchForm(FlaskForm):
    """City or zipcode form"""
    zipcode = IntegerField('Zipcode', validators=[InputRequired()])
    # https://wtforms.readthedocs.io/en/2.3.x/validators/#wtforms.validators.InputRequired
    # TODO maybe add a custom validator for zipcodes