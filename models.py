"""SQLAlchemy models for want2go"""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()
def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text,nullable=False)
    email = db.Column(db.Text,nullable=False,unique=True)
    password = db.Column(db.Text,nullable=False)

    likes = db.relationship('Restaurant', secondary="likes")
    dislikes = db.relationship('Restaurant', secondary="dislikes")
    areas = db.relationship('Area',secondary="areas")

    def __repr__(self):
        return f"<User #{self.id}: {self.name}, {self.email}>"
    
    @classmethod
    def signup(cls,name,email,password):
        '''Sign up user.
        Hashes password and adds user to db
        '''
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user=User(name=name,email=email,password=hashed_pwd)
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls,email,password):
        '''Find user with email and password.

        if can't find matching user, or wrong, return false
        otherwise, returns user.
        '''
        user = cls.query.filter_by(email=email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password,password)
            if is_auth:
                return user
        return False

class Likes(db.Model):
    """Mapping user likes to restaurants"""
    __tablename__ = "likes"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id', ondelete='cascade'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id', ondelete='cascade'),unique=True)
    
    user = db.relationship('User')

class Dislikes(db.Model):
    """Mapping user dislikes to restaurants"""
    __tablename__ = "dislikes"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id', ondelete='cascade'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id', ondelete='cascade'),unique=True)
    
    user = db.relationship('User')

class Restaurant(db.Model):
    """An individule restaurant"""
    __tablename__ = "restaurants"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text,nullable=False)
    address = db.Column(db.Text,nullable=False)
    description = db.Column(db.Text,nullable=False)
    city = db.Column(db.Text,nullable=False)
    state = db.Column(db.Text,nullable=False)
    google_place_id = db.Column(db.Text,nullable=False)

class Area(db.Model):
    """An area a user swipes in"""
    __tablename__ = "areas"
    id = db.Column(db.Integer,primary_key=True)
    zipcode = db.Column(db.Integer,nullable=False)

    