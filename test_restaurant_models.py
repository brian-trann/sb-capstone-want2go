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


        area_2 = Area(city="Irvine", state="CA")
        self.user_3.areas.append(area_2)
        db.session.commit()
        self.area_2 = area_2

        d = {"googlePlaceId":"ChIJ9f9zhYDb3IARfXSrxrDSdq4","name":"Lazy Dog Restaurant & Bar","address":"address"}
        rest_2 = Restaurant(name=d['name'],address=d['address'], google_place_id=d['googlePlaceId'],user_id=self.user_1.id, area_id=self.area_2.id)
        db.session.add(rest_2)
        db.session.commit()
        self.rest_2 = rest_2

    def tearDown(self):
        """Clean up db or any bad transaction """
        db.session.rollback()
    
    def test_restaurant_model(self):
        """ Testing basic restaurant model"""
        d = {"googlePlaceId":"ChIJ9f9zhYDb3IARfXSrxrDSdq4","name":"Lazy Dog Restaurant & Bar","address":"address"}
        rest_1 = Restaurant(name=d['name'],address=d['address'], google_place_id=d['googlePlaceId'],user_id=self.user_3.id, area_id=self.area_2.id)
        db.session.add(rest_1)
        db.session.commit()
        restaurant = Restaurant.query.get(rest_1.id)
        self.assertIsNotNone(restaurant)

    def test_restaurant_serialize(self):
        r_serialized = {"id":self.rest_2.id,
                "name":self.rest_2.name,
                "address":self.rest_2.address,
                "google_place_id":self.rest_2.google_place_id,
                "area_id":self.rest_2.area_id,
                "area_city":self.rest_2.area.city,
                "area_state":self.rest_2.area.state
        }
        self.assertEqual(self.rest_2.serialize(),r_serialized)