import os
from flask import Flask, render_template, request, redirect, session, g, flash, jsonify
from api import api
from flask_debugtoolbar import DebugToolbarExtension
from forms import UserAddForm, LoginForm, SearchForm
from models import db, User,Likes, Dislikes, Restaurant, Area, UserAreas
from sqlalchemy.exc import IntegrityError


from models import db, connect_db

CURR_USER_KEY = "curr_user"
CURR_USER_AREA = 'curr_area'

app = Flask(__name__)
app.register_blueprint(api,url_prefix="/api")

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///want2go_test'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
# toolbar = DebugToolbarExtension(app)

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
    '''Sets an area ID to the session. This will be used to make a request to place_search_request()'''
    session[CURR_USER_AREA] = area_id

def do_reset_area():
    '''Removes the area id from the session '''
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
            flash("Email already in use!", 'danger')
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
    """ If the city and state is good: make request here. """
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    if CURR_USER_AREA not in session:
        return redirect('/areas')

    area = Area.query.get_or_404(session[CURR_USER_AREA])    

    return render_template('/restaurants/restaurants.html',area=area)


@app.route('/discover/restaurants/<int:area_id>')
def discover_restaurant_in_area(area_id):
    '''This route sets an area in the session where restaurant discoveries will occur '''
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    do_set_area(area_id)
    return redirect('/discover/restaurants')


@app.route('/likes')
def restaurant_likes():
    """Table showing all restaurants??? """
    if not g.user:
        return redirect("/")
    return render_template('likes.html')

@app.route('/areas', methods=["GET","POST"])
def show_areas():
    '''Route to show a user's areas '''
    if not g.user:
        return redirect("/")

    user_areas = Area.query.filter(UserAreas.user_id ==g.user.id).all()
    user = User.query.get_or_404(g.user.id)
    form = SearchForm()
    user_cities = [area.serialize() for area in user_areas]

    if form.validate_on_submit():
        city = form.city.data
        state = form.state.data
        formatted_city = city.title()

        for area in user_cities:
            if area['city'] == formatted_city and area['state'] == state:
                area_id = area['id']
                flash('You already added this area!','success')
                return redirect(f'/discover/restaurants/{area_id}')
                
        area = Area(city=formatted_city,state=state)
        g.user.areas.append(area)
        db.session.commit()
        return redirect(f'/discover/restaurants/{area.id}')
    return render_template('/areas/areas.html',form=form)

@app.route('/areas/<int:area_id>/delete')
def delete_area(area_id):
    '''Route to delete a user's area'''
    if not g.user:
        return redirect('/')
    area = Area.query.get_or_404(area_id)
    g.user.areas.remove(area)
    db.session.delete(area)
    db.session.commit()
    return redirect('/areas')

