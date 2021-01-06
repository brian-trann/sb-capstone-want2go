import os
from flask import Flask, render_template, request, redirect, session, g, flash
from flask_debugtoolbar import DebugToolbarExtension

# from forms import UserAddForm, LoginForm, MessageForm, EditUserForm
from models import db, connect_db

# CURR_USER_KEY = "curr_user"

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