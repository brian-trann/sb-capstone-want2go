"""Test API Routes - Authorized User"""

import os
from unittest import TestCase
from flask import session
from models import db, User, Likes, Dislikes, Restaurant, Area, UserAreas

os.environ['DATABASE_URL'] = "postgresql:///want2go_test_db"
from app import app, CURR_USER_KEY, CURR_USER_AREA

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False

UNAUTHORIZED = {"message":"Unauthorized"}

db.create_all()

class ApiAuthorizedTestCase(TestCase):
    """ Test API for authorized user."""
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

        area_1 = Area(city="Irvine", state="CA")
        self.user_2.areas.append(area_1)
        db.session.commit()
        self.area_1 = area_1

        area_2 = Area(city="Irvine", state="CA")
        self.user_3.areas.append(area_2)
        db.session.commit()
        self.area_2 = area_2

        d = {"googlePlaceId":"ChIJ9f9zhYDb3IARfXSrxrDSdq4","name":"Lazy Dog Restaurant & Bar","address":"address"}
        rest_1 = Restaurant(name=d['name'],address=d['address'], google_place_id=d['googlePlaceId'],user_id=self.user_3.id, area_id=self.area_2.id)
        db.session.add(rest_1)
        db.session.commit()
        self.rest_1 = rest_1
        like = Likes(user_id=user_3.id, restaurant_id=rest_1.id)
        db.session.add(like)
        db.session.commit()

    def tearDown(self):
        """ Clean up bad transactions. """
        db.session.rollback()

    def test_api_areas(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_2.id
            resp = client.get('/api/areas')
            self.assertEqual(resp.status_code,200)
            data = resp.json
            for area in data['areas']:
                self.assertIsInstance(area['id'],int)
                self.assertEqual(area['city'],str)
                self.assertIsInstance(area['state'],str)
    
    def test_api_restaurants(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_2.id
                sess[CURR_USER_AREA] = self.area_1.id
            resp = client.get('/api/restaurants')
            self.assertEqual(resp.status_code,200)
            data = resp.json
            self.assertIsInstance(data['place_ids'], list)
            self.assertIsInstance(data['next_page_token'], str)]


    def test_api_get_restaurant_details(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_2.id
                sess[CURR_USER_AREA] = self.area_1.id
            d = {"restaurantPlaceId":"ChIJ9f9zhYDb3IARfXSrxrDSdq4"}

            resp = client.post('/api/restaurant/details', json=d)
            data = resp.json
            self.assertIsInstance(data['status'], str)
            self.assertIsInstance(data['details'], dict)
            self.assertIsInstance(data['details']['google_place_id'], str)
            self.assertIsInstance(data['details']['name'], str)
            self.assertIsInstance(data['details']['address'], str)
            self.assertIsInstance(data['details']['photo_references'], list)
    
    def test_api_get_restaurant_photo(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_2.id
            d = {"photo_reference":"ATtYBwJNaphKhV3CwyIPym5-nNqGknIIBcH-XcY81BErFJY3oKL121r1DBUxnNWBtLBblrKZNu92pGqHoYq4USejEURdCI1rjrtMzGwNva_OfZ02Y-D1Qn43dsMiw8uECfPnU99aTyVRWzqUxgW-LCAQYmAa8zRcdon76qWNN27zUAEMWwV7"}

            resp = client.post('/api/restaurant/details/photo', json=d)
            data = resp.json
            self.assertIsInstance(data['url'], str)

    def test_like_restaurant(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_2.id
                sess[CURR_USER_AREA] = self.area_1.id
            d = {"googlePlaceId":"ChIJ9f9zhYDb3IARfXSrxrDSdq4","name":"Lazy Dog Restaurant & Bar","address":"address"}

            resp = client.post('/api/restaurant/like', json=d)
            data = resp.json
            user = User.query.get_or_404(self.user_2.id)
            user_likes = [restaurant for restaurant in user.likes]
            self.assertEqual(len(user_likes),1)
            self.assertEqual(data,{"restaurant":"liked"})

    def test_dislike_restaurant(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_2.id
                sess[CURR_USER_AREA] = self.area_1.id
            d = {"googlePlaceId":"ChIJ9f9zhYDb3IARfXSrxrDSdq4","name":"Lazy Dog Restaurant & Bar","address":"address"}

            resp = client.post('/api/restaurant/dislike', json=d)
            data = resp.json
            user = User.query.get_or_404(self.user_2.id)
            user_dislikes = [restaurant for restaurant in user.dislikes]
            self.assertEqual(len(user_dislikes),1)
            self.assertEqual(data,{"restaurant":"disliked"})

    def test_unlike_restaurant(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_3.id
                sess[CURR_USER_AREA] = self.area_2.id
            d = {"googlePlaceId":"ChIJ9f9zhYDb3IARfXSrxrDSdq4"}

            user = User.query.get_or_404(self.user_3.id)
            user_likes = [restaurant for restaurant in user.likes]
            self.assertEqual(len(user_likes),1)

            resp = client.post('/api/restaurant/unlike',json=d)
            data = resp.json
            user_after = User.query.get_or_404(self.user_3.id)
            user_after_likes = [restaurant for restaurant in user.likes]
            self.assertEqual(len(user_after_likes),0)
            self.assertEqual(data,{"restaurant":"unliked"})

    def test_get_likes_dislikes(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_3.id
                
            resp = client.get('/api/user/likes')
            data = resp.json
            self.assertIsInstance(data['likes'],list)
            self.assertIsInstance(data['dislikes'],list)
            self.assertEqual(len(data['likes']),1)
            self.assertEqual(len(data['dislikes']),0)