
""" test_parcel_delivery_orders.py File to test parcel order endpoints"""
import sys
sys.path.append('../.')
import unittest
import json
from app import app
from database import DatabaseConnection

database = DatabaseConnection()

class test_parcel_orders(unittest.TestCase):
    """test_class"""

    def setUp(self):
        """set up params"""
        self.test = app.test_client()
        self.parcel = { "date": "date", "destination": "destination", "parcelSize": "parcelSize", "pickupLocation": "pickupLocation", "price": "200", "status": "in transit", "userid": 1 }
        self.user = {"userid":1, "name":"admin", "username":"test2", "password":"admin"}
        database.drop_tables()
        database.create_tables()
        database.default_user()
        self.test.post("/api/v1/signup", headers={"Content-Type": "application/json"}, data=json.dumps(self.user))
        response = self.test.post('/api/v1/login', data=json.dumps({"username":"admin", "password":"admin"}), content_type='application/json')
        data = json.loads(response.data)
        token = data.get('access_token')
        self.headers = {"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}

    def tearDown(self):
        """tear down params"""
        self.test = None
        self.parcel = None

    #test index route loads
    def test_index_page_loads(self):
        """test index page"""
        response = self.test.get('/', headers=self.headers)
        self.assertEqual(response.status_code, 200)

    #test get parcels route loads
    def test_get_parcels_loads(self):
        """test parcels page"""
        response = self.test.get('/api/v1/parcels', headers=self.headers)
        self.assertEqual(response.status_code, 400)

    #test posting an empty parcel
    def test_post_empty_parcels(self):
        """parcels page with empty list"""
        response = self.test.post('/api/v1/parcels', headers=self.headers)
        self.assertEqual(response.status_code, 400)

    #test posting an empty user
    def test_post_empty_user(self):
        """user page with empty list"""
        response = self.test.post('/api/v1/signup', headers=self.headers)
        self.assertEqual(response.status_code, 400)

    #test get parcel by id
    def test_get_parcel_by_id(self):
        """get a parcel by its id"""
        response = self.test.get('/api/v1/parcels/3', headers=self.headers)
        self.assertEqual(response.status_code, 400)

    #test get user by id
    def test_get_user_by_id(self):
        """get a user by id"""
        response = self.test.get('/api/v1/users/1', headers=self.headers)
        self.assertTrue(b'username' in response.data)
        self.assertEqual(response.status_code, 200)

    #test get parcel by userid
    def test_get_parcel_by_userid(self):
        """get parcels by user id"""
        response = self.test.get('/api/v1/users/4/parcels', headers=self.headers)
        self.assertEqual(response.status_code, 400)

    #test posting with parcel data
    def test_post_data_parcels(self):
        """posting parcel data"""
        self.user["username"] = "test4"
        self.test.post("/api/v1/signup", headers=self.headers, data=json.dumps(self.user))
        res = self.test.post("/api/v1/parcels", headers=self.headers, data=json.dumps(self.parcel))
        self.assertEqual(res.status_code, 201)
        self.assertTrue(b'status' in res.data)

    #test posting user data
    def test_post_data_users(self):
        """posting user data"""
        self.user["username"] = "test3"
        res = self.test.post("/api/v1/signup", headers={"Content-Type": "application/json"}, data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        self.assertTrue(b'username' in res.data)

    #test cancel parcel
    def test_cancel_parcel(self):
        """cancel a parcel"""
        response = self.test.put('/api/v1/parcels/3/cancel', headers=self.headers)
        self.assertEqual(response.status_code, 400)
