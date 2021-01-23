"""Test User Model"""

import os
from unittest import TestCase
from flask import session
from models import db, User, Likes, Dislikes, Restaurant, Area, UserAreas

os.environ['DATABASE_URL'] = "postgresql:///want2go_test_db"
from app import app, CURR_USER_KEY, CURR_USER_AREA

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False

db.create_all()

class UserModel(TestCase):
    '''Testing the model for user.'''

    def setUp(self):
        db.drop_all()
        db.create_all()
        self.client = app.test_client()
        user_1 = User.signup("user1",'user1@gmail.com','password')
        user_2 = User.signup("user2",'user2@gmail.com','password')
        user_3 = User.signup("user3",'user3@gmail.com','password')

        db.session.add_all([user_1,user_2,user_3])
        db.session.commit()
        self.user_1 = user_1
        self.user_2 = user_2
        self.user_3 = user_3

    def tearDown(self):
        """Clean up db or any bad transaction """
        db.session.rollback()

    def test_user_model(self):
        """Does the basic user model work?"""
        user = User(email="test_user@gmail.com",name="Testing User", password="thisisatest")
        db.session.add(user)
        db.session.commit()
        self.assertEqual(len(user.areas),0)
        self.assertEqual(len(user.likes),0)
        self.assertEqual(len(user.dislikes),0)

    def test_user_repr(self):
        """Test representation of user"""
        u1_repr =f"<User #{self.user_1.id}: {self.user_1.name}, {self.user_1.email}>"
        u2_repr =f"<User #{self.user_2.id}: {self.user_2.name}, {self.user_2.email}>"
        u3_repr =f"<User #{self.user_3.id}: {self.user_3.name}, {self.user_3.email}>"
        self.assertEqual(self.user_1.__repr__(), u1_repr)
        self.assertEqual(self.user_2.__repr__(), u2_repr)
        self.assertEqual(self.user_3.__repr__(), u3_repr)
    
    def test_user_signup(self):
        """ Testing signup functionality"""
        valid_user = User.signup("Valid","valid@gmail.com",'thisisatest')
        db.session.add(valid_user)
        db.session.commit()
        user = User.query.get(valid_user.id)
        self.assertIsNotNone(user)
        self.assertEqual(user.name, valid_user.name)
        self.assertEqual(user.email, valid_user.email)

    def test_user_authenticate_success(self):
        user_1 = User.authenticate(self.user_1.email,'password')
        user_2 = User.authenticate(self.user_2.email,'password')
        self.assertEqual(user_1.id , self.user_1.id)
        self.assertEqual(user_2.id , self.user_2.id)
    
    def test_user_authenticate_success(self):
        user_1 = User.authenticate(self.user_1.email,'fake_password')
        user_2 = User.authenticate(self.user_2.email,'fake_password')
        self.assertFalse(user_1)
        self.assertFalse(user_2)