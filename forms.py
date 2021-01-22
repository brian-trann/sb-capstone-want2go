from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField
from wtforms.validators import InputRequired, Email, Length, ValidationError


states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
          
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
    # zipcode = StringField('Zipcode', validators=[InputRequired(), check_zipcode])
    city = StringField('City', validators=[InputRequired()])
    state = SelectField('State', choices=[(st, st) for st in states])
    # https://wtforms.readthedocs.io/en/2.3.x/validators/#wtforms.validators.InputRequired
    

