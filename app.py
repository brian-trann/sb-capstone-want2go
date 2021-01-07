import os
from flask import Flask, render_template, request, redirect, session, g, flash
from flask_debugtoolbar import DebugToolbarExtension
from forms import UserAddForm, LoginForm, SearchForm
from sqlalchemy.exc import IntegrityError
import zipcodes

# from forms import UserAddForm, LoginForm, MessageForm, EditUserForm
from models import db, connect_db

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///want2go_test'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

##########################################################
# User signup/login/logout

@app.route('/')
def index():
    """Basic setup of app. Will rename."""
    return render_template('index.html')

@app.route('/signup', methods=["GET","POST"])
def signup():
    """Handle user signup. Create new user -> add to DB -> redirect.
    If form not valid, present form.
    If user exists, flash message and re-present
    """
    form = UserAddForm()

    if form.validate_on_submit():
        return "Correct"
    
    else:
        return render_template('/users/signup.html',form=form)

@app.route('/login', methods=["GET","POST"])
def login():
    """Handle user login."""
    form = LoginForm()

    if form.validate_on_submit():
        return "Correct"
    
    else:
        return render_template('/users/login.html',form=form)

@app.route('/discover',methods=["GET","POST"])
def discover():
    """Handle restaurant discovery"""
    form = SearchForm()
    if form.validate_on_submit():
        return redirect('/restaurants')

    return render_template('discover.html', form=form)

@app.route('/search', methods=["POST"])
def search():
    """Handle zipcode search"""

    return redirect('/restaurants')

@app.route('/restaurants')
def discover_restaurants():
    """ If the zipcode is good: """
    return render_template('/restaurants/restaurants.html')