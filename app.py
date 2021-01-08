import os
from flask import Flask, render_template, request, redirect, session, g, flash
from flask_debugtoolbar import DebugToolbarExtension
from forms import UserAddForm, LoginForm, SearchForm
from models import db, User,Likes, Dislikes, Restaurant
from sqlalchemy.exc import IntegrityError
from secrets import PRIVATE_API_KEY
from helpers import place_search_request
import zipcodes

# from forms import UserAddForm, LoginForm, MessageForm, EditUserForm
from models import db, connect_db

CURR_USER_KEY = "curr_user"
TEMP_LAT = "42.3675294"
TEMP_LONG = "-71.186966"

app = Flask(__name__)
# db.create_all()
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
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout; delete from session"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
##########################################################

@app.route('/')
def index():
    """Basic setup of app. Will rename."""
    #if g.user: redirect to discover.
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
        user = User
        return "Correct"
    
    else:
        return render_template('/users/login.html',form=form)

@app.route('/discover',methods=["GET","POST"])
def discover():
    """Handle restaurant discovery"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = SearchForm()
    if form.validate_on_submit():
        # TODO validate zipcode
        user_zipcode = form.zipcode.data
        matched_zip = zipcodes.matching(user_zipcode) 
        #maybe make a handleMatchedZipcodes()
        latitude = matched_zip[0]['lat']
        longitude = matched_zip[0]['long']
        city = matched_zip[0]['city'] # saving this value, maybe put into db
        res = place_search_request(latitude=latitude,longitude=longitude,key=PRIVATE_API_KEY)
        #TODO Figure out if i should save this to the session,
        return redirect('/restaurants')

    return render_template('discover.html', form=form)

@app.route('/search', methods=["POST"])
def search():
    """Handle zipcode search"""

    return redirect('/restaurants')

@app.route('/restaurants')
def discover_restaurants():
    """ If the zipcode is good: make request here. """
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    return render_template('/restaurants/restaurants.html')

@app.route('/cities')
def cities():
    """If cities is clicked, query DB for all of user's cities
    add button cities - > form to add a new place
    If no cities; show form to add cities
    TODO
    """
    return render_template('index.html')

@app.route('/restaurant/likes')
def restaurant_likes():
    """Table showing all restaurants??? 
    TODO IDK about this route yet
    """
    return render_template('index.html')