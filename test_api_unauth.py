"""Test API Routes"""

import os
from unittest import TestCase
from flask import session
from models import db

os.environ['DATABASE_URL'] = "postgresql:///want2go_test_db"
from app import app

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False

db.create_all()

UNAUTHORIZED = {"message":"Unauthorized"}

class ApiTestCase(TestCase):
    """ Test API for Unauthorized user. All response codes should be 401"""
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        """ Clean up bad transactions. """
        db.session.rollback()

    def test_api_areas(self):
        with self.client as client:
            resp = client.get('/api/areas')
            self.assertEqual(resp.status_code,401)
            data = resp.json
            self.assertEqual(data,UNAUTHORIZED)

    def test_api_restaurants(self):
        with self.client as client:
            resp = client.get('/api/restaurants')
            self.assertEqual(resp.status_code,401)
            data = resp.json
            self.assertEqual(data,UNAUTHORIZED)
            
    def test_api_restaurants_nextpage(self):
        with self.client as client:
            resp = client.post('/api/restaurants/nextpage')
            self.assertEqual(resp.status_code,401)
            data = resp.json
            self.assertEqual(data,UNAUTHORIZED)
    def test_api_restaurant_details(self):
        with self.client as client:
            resp = client.post('/api/restaurant/details')
            self.assertEqual(resp.status_code,401)
            data = resp.json
            self.assertEqual(data,UNAUTHORIZED)

    def test_api_restaurant_details_photo(self):
        with self.client as client:
            resp = client.post('/api/restaurant/details/photo')
            self.assertEqual(resp.status_code,401)
            data = resp.json
            self.assertEqual(data,UNAUTHORIZED)
            
    def test_api_restaurant_like(self):
        with self.client as client:
            resp = client.post('/api/restaurant/like')
            self.assertEqual(resp.status_code,401)
            data = resp.json
            self.assertEqual(data,UNAUTHORIZED)

    def test_api_restaurant_unlike(self):
        with self.client as client:
            resp = client.post('/api/restaurant/unlike')
            self.assertEqual(resp.status_code,401)
            data = resp.json
            self.assertEqual(data,UNAUTHORIZED)

    def test_api_restaurant_dislike(self):
        with self.client as client:
            resp = client.post('/api/restaurant/dislike')
            self.assertEqual(resp.status_code,401)
            data = resp.json
            self.assertEqual(data,UNAUTHORIZED)

    def test_api_user_likes(self):
        with self.client as client:
            resp = client.get('/api/user/likes')
            self.assertEqual(resp.status_code,401)
            data = resp.json
            self.assertEqual(data,UNAUTHORIZED)

    def test_api_likes(self):
        with self.client as client:
            resp = client.get('/api/likes')
            self.assertEqual(resp.status_code,401)
            data = resp.json
            self.assertEqual(data,UNAUTHORIZED)
