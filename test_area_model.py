"""Test Restaurant Model"""

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

class UserMode(TestCase):
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

        area_test = Area(city="Irvine", state="CA")
        self.user_1.areas.append(area_test)
        db.session.commit()
        self.area_test = area_test

    def tearDown(self):
        """Clean up db or any bad transaction """
        db.session.rollback()
    
    def test_area_model(self):
        area = Area(city="Los Angeles", state="CA")
        db.session.add(area)
        db.session.commit()
        check_area = Area.query.get(area.id)
        self.assertIsNotNone(check_area)
    
    def test_area_seralize(self):
        area_seralized = {"id":self.area_test.id,"city":self.area_test.city,"state":self.area_test.state}
        self.assertEqual(self.area_test.serialize(), area_seralized)