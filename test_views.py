"""User Views tests"""

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


class UserViewsTestCase(TestCase):
    """ Test Views for user. """

    def setUp(self):
        """ Create test client, add sample data."""
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
    
    def tearDown(self):
        """Clean up db or any bad transaction """
        db.session.rollback()

    def test_root(self):
        with self.client as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1 class="display-4">want2go</h1>',html)

    def test_get_signup(self):
        with self.client as client:
            resp = client.get('/signup')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('<button class="btn btn-primary btn-lg btn-block">Sign me up!</button>', html)

    def test_post_signup(self):
        with self.client as client:
            d = {"name":"user_test", "email":"user_test@gmail.com","password":"password"}
            resp = client.post('/signup', data=d)
            html= resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,302)

    def test_post_signup_follow_redirect(self):
        with self.client as client:
            d = {"name":"user_test", "email":"user_test@gmail.com","password":"password"}
            resp = client.post('/signup', data=d,follow_redirects=True)
            html= resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('<p class="mt-5 h5 ">Places you are looking</p>',html)
            
    def test_get_login(self):
        with self.client as client:
            resp = client.get('/login')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('<button class="btn btn-primary btn-lg btn-block">Log in</button>',html)

    def test_post_login(self):
        with self.client as client:
            d = {"email":"user1@gmail.com","password":"password"}
            resp = client.post('/login',data=d)
            self.assertEqual(resp.status_code,302)

    def test_post_login_follow_redirect(self):
        with self.client as client:
            d = {"email":"user1@gmail.com","password":"password"}
            resp = client.post('/login',data=d,follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('<p class="mt-5 h5 ">Places you are looking</p>',html)
    
    def test_post_login_wrong_pw(self):
        with self.client as client:
            d = {"email":"user1@gmail.com","password":"wrong"}
            resp = client.post('/login',data=d)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('<button class="btn btn-primary btn-lg btn-block">Log in</button>',html)

    def test_logout(self):
        with self.client as client:
            resp =client.get('/logout')
            self.assertEqual(resp.status_code,302)

    def test_auth_discover(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY]= self.user_1.id
            resp = client.get('/discover',follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('<p class="mt-5 h5 ">Places you are looking</p>',html)
    
    def test_auth_discover_with_area(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_2.id
                sess[CURR_USER_AREA] = self.area_1.id
            resp = client.get('/discover',follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('Irvine, CA</p>',html)
            
    def test_unauth_discover(self):
        with self.client as client:
            resp =client.get('/discover')
            self.assertEqual(resp.status_code,302)
    
    def test_unauth_discover_follow_redirect(self):
        with self.client as client:
            resp =client.get('/discover',follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1 class="display-4">want2go</h1>',html)
            
    
    def test_unauth_discover_restaurants(self):
        with self.client as client:
            resp =client.get('/discover/restaurants')
            self.assertEqual(resp.status_code,302)
    
    def test_unauth_discover_restaurants_follow_redirect(self):
        with self.client as client:
            resp =client.get('/discover/restaurants',follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1 class="display-4">want2go</h1>',html)
    

    def test_unauth_likes(self):
        with self.client as client:
            resp =client.get('/likes')
            self.assertEqual(resp.status_code,302)
    
    def test_unauth_likes_follow_redirect(self):
        with self.client as client:
            resp =client.get('/likes',follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1 class="display-4">want2go</h1>',html)
    
    def test_auth_areas(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY]= self.user_1.id
            resp = client.get('/areas',follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('<div class="row justify-content-md-center my-5" id="areas-table">',html)

    def test_auth_areas_post(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY]= self.user_1.id
            d = {"city":"Irvine","state":"CA"}
            resp = client.post('/areas',follow_redirects=True,data=d)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('Irvine, CA</p>',html)

    def test_unauth_areas(self):
        with self.client as client:
            resp =client.get('/areas')
            self.assertEqual(resp.status_code,302)
    
    def test_unauth_areas_follow_redirect(self):
        with self.client as client:
            resp =client.get('/areas',follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1 class="display-4">want2go</h1>',html)
    
    def test_auth_area_delete(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user_2.id
                sess[CURR_USER_AREA] = self.area_1.id
            resp = client.get(f'/areas/{self.area_1.id}/delete',follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertNotIn('Irvine, CA', html)
