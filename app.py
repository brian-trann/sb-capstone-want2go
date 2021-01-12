import os
from flask import Flask, render_template, request, redirect, session, g, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from forms import UserAddForm, LoginForm, SearchForm
from models import db, User,Likes, Dislikes, Restaurant, Area, UserAreas
from sqlalchemy.exc import IntegrityError
from secrets import PRIVATE_API_KEY
from helpers import place_search_request
import zipcodes

# from forms import UserAddForm, LoginForm, MessageForm, EditUserForm
from models import db, connect_db

CURR_USER_KEY = "curr_user"
CURR_USER_AREA = ''


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

def do_set_area(area_id):
    session[CURR_USER_AREA] = area_id

def do_reset_area():
    if CURR_USER_AREA in session:
        del session[CURR_USER_AREA]
##########################################################

@app.route('/')
def index():
    """Basic setup of app. Will rename."""
    #if g.user: redirect to discover.
    if g.user:
        return redirect('/discover')
    return render_template('index.html')

@app.route('/signup', methods=["GET","POST"])
def signup():
    """Handle user signup. Create new user -> add to DB -> redirect.
    If form not valid, present form.
    If user exists, flash message and re-present
    """
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                name=form.name.data,
                email=form.email.data,
                password=form.password.data
            )
            db.session.commit()
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('/users/signup.html',form=form)
        do_login(user)
        return redirect('/')

    else:
        return render_template('/users/signup.html',form=form)

@app.route('/login', methods=["GET","POST"])
def login():
    """Handle user login."""
    form = LoginForm()
    if g.user:
        return redirect('/')
    if form.validate_on_submit():
        user = User.authenticate(form.email.data,form.password.data)
        if user:
            do_login(user)
            flash("You've logged in!", 'success')
            return redirect('/discover')
        flash('Invalid credentials.', 'danger')
    
    return render_template('/users/login.html',form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_reset_area()
    do_logout()
    return redirect('/')

@app.route('/discover')
def discover():
    """Handle restaurant discovery"""
    if not g.user:
        return redirect("/")
    areas = Area.query.filter(UserAreas.user_id ==g.user.id).all()
    if not areas:
        return redirect('/areas')
    else:
        return redirect('/discover/restaurants')


@app.route('/discover/restaurants')
def discover_restaurants():
    """ If the zipcode is good: make request here. """
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    if session[CURR_USER_AREA] == '':
        flash("Pick an area first!", 'success')
        return redirect('/areas')
    elif CURR_USER_AREA in session:
        area = Area.query.get_or_404(session[CURR_USER_AREA])
    
    response = place_search_request(latitude=area.latitude,longitude=area.longitude,key=PRIVATE_API_KEY)
    handleSearchResponse(response)
    # if len(session['place_ids']) < 0:
    ### make a place_details_request with first element in session['place_ids']
    # make this a json response instead of returning an HTML template. 
    #split out the API and the actual APP. it'll call this route, and get the info.
    return render_template('/restaurants/restaurants.html',area=area)


@app.route('/discover/restaurants/<int:area_id>')
def discover_restaurant_in_area(area_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    do_set_area(area_id)
    return redirect('/discover/restaurants')


@app.route('/restaurant/likes')
def restaurant_likes():
    """Table showing all restaurants??? 
    TODO IDK about this route yet
    """
    return render_template('index.html')

@app.route('/areas', methods=["GET","POST"])
def show_areas():
    if not g.user:
        return redirect("/")

    user = User.query.get_or_404(g.user.id)
    form = SearchForm()
    user_zipcodes = [str(area.zipcode) for area in user.areas]

    if form.validate_on_submit():
        user_zipcode = form.zipcode.data
        if user_zipcode in user_zipcodes:
            flash('You already added this area','danger')
            return render_template('/areas/areas.html',form=form,areas=user.areas)

        matched_zip = zipcodes.matching(user_zipcode)
        latitude = matched_zip[0]['lat']
        longitude = matched_zip[0]['long']
        city = matched_zip[0]['city'] 
        state = matched_zip[0]['state'] 
        area = Area(zipcode=user_zipcode,city=city,state=state,latitude=latitude,longitude=longitude)
        g.user.areas.append(area)
        db.session.commit()
        return redirect(f'/discover/restaurants/{area.id}')
    return render_template('/areas/areas.html',areas=user.areas,form=form)

@app.route('/areas/<int:area_id>/delete')
def delete_area(area_id):
    if not g.user:
        return redirect('/')
    area = Area.query.get_or_404(area_id)
    g.user.areas.remove(area)
    db.session.delete(area)
    db.session.commit()
    return redirect('/areas')

def handleSearchResponse(response):
    """Handles response from Google Search API, adds to session"""
    session['place_ids'] = response['place_ids']
    session['next_page_token'] = response['next_page_token']