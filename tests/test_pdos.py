
"""test_pdos.py File to test parcel order endpoints"""
import sys
sys.path.append('../')
from app import app
import unittest
import json
import pytest
from database import DatabaseConnection

database = DatabaseConnection()
database.drop_tables()
database.create_tables()

class test_parcel_orders(unittest.TestCase):
    
    def setUp(self):
        """set up params"""
        self.test = app.test_client()
        self.test.get('/parcels/cancel')
        self.test.get('/users/cancel')
        database.drop_tables()
        database.create_tables()
        database.default_user()
        self.parcel = { "date": "date", "destination": "destination", "parcelSize": "parcelSize", "pickupLocation": "pickupLocation", "price": "200", "status": "in transit", "userid": 1 }
        self.user = {"name":"admin", "username":"test", "password":"admin"}
        self.test.post("/api/v1/signup", headers={"Content-Type": "application/json"}, data=json.dumps(self.user))
        response = self.test.post('/api/v1/login', data=json.dumps({"username":"admin", "password":"admin"}), content_type='application/json')
        data = json.loads(response.data)
        token = data.get('access_token')
        self.headers = {"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}
        self.test.post("/api/v1/parcels", headers=self.headers, data=json.dumps(self.parcel))

    def tearDown(self):
        """tear down params"""
        self.test = None
        self.parcel = None

    #test cancel a parcel loads the data?
    def test_cancel_parcel_loads_data(self):
        """testing cancel parcel with data"""
        response = self.test.put('/api/v1/parcels/1/cancel', headers=self.headers)
        #self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Cancelled' in response.data)

    #test login
    def test_login(self):
        """testing login"""
        response = self.test.post('/api/v1/login', data=json.dumps({"username":"admin", "password":"admin"}), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    #test user signup
    def test_signup(self):
        """user signup"""
        response = self.test.post("/api/v1/signup", headers={"Content-Type": "application/json"}, data=json.dumps({"name":"admin", "username":"signup", "password":"admin"}))
        self.assertTrue(b'username' in response.data)
        self.assertEqual(response.status_code, 201)

    #test get parcels route loads the data
    def test_get_parcels_loads_data(self):
        """test loading parcel data"""
        response = self.test.get('/api/v1/parcels', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'status' in response.data)

    # #test get parcels route by id loads the data
    def test_get_parcel_by_id_loads_data(self):
        """picking a parcel with data"""
        response = self.test.get('/api/v1/parcels/1', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'status' in response.data)

    #test get parcels route by userid loads the data
    def test_get_parcel_by_userid_loads_data(self):
        """picking parcels with userid"""
        response = self.test.get('/api/v1/users/2/parcels', headers=self.headers)
        self.assertTrue(b'status' in response.data)

    #test get users route loads the data
    def test_get_users_loads_data(self):
        """test loading users data"""
        response = self.test.get('/api/v1/users', headers=self.headers)
        self.assertTrue(b'username' in response.data)

    # #test get users route by id loads the data
    def test_get_user_by_id_loads_data(self):
        """picking a user with data"""
        response = self.test.get('/api/v1/users/1', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'username' in response.data)