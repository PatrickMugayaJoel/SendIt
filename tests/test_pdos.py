
"""
test_pdos.py File to test parcel order endpoints
"""
import sys
sys.path.append('../')
from app import app
import unittest
import json
import pytest

class test_parcel_orders(unittest.TestCase):
    def setUp(self):
        """
        set up params
        """
        self.test = app.test_client()
        self.test.get('/parcels/cancel')
        self.test.get('/users/cancel')
        self.parcel = {"orderID":"DO_1", "status":"in transit", "userid":1}
        self.user = {"userid":"DO_1", "username":"Josean", "password":"password", "role":"Admin"}
        self.test.post("/api/v1/users", headers={"Content-Type": "application/json"}, data=json.dumps(self.user))
        self.test.post("/api/v1/parcels", headers={"Content-Type": "application/json"}, data=json.dumps(self.parcel))

    def tearDown(self):
        """
        tear down params
        """
        self.test = None
        self.parcel = None

    #test cancel a parcel loads the data?
    def test_cancel_parcel_loads_data(self):
        """
        testing cancel parcel with data
        """
        response = self.test.put('/api/v1/parcels/1/cancel')
        res_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        expected_output = {'orderID': 1, 'status': 'Canceled', 'userid': 1}
        self.assertEqual(res_data, expected_output)

    #test get parcels route loads the data
    def test_get_parcels_loads_data(self):
        """
        test loading parcel data
        """
        response = self.test.get('/api/v1/parcels')
        res_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'status' in response.data)
        expected_output = [{'orderID': 1, 'userid': 1, 'status': 'in transit'}]
        self.assertEqual(res_data, expected_output)

    #test get parcels route by id loads the data
    def test_get_parcel_by_id_loads_data(self):
        """
        picking a parcel with data
        """
        response = self.test.get('/api/v1/parcels/1')
        res_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        expected_output = [{'orderID': 1, 'userid': 1, 'status': 'in transit'}]
        self.assertEqual(res_data, expected_output)

    #test get parcels route by userid loads the data
    def test_get_parcel_by_userid_loads_data(self):
        """
        picking parcels with userid
        """
        response = self.test.get('/api/v1/users/1/parcels')
        res_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        expected_output = [{'orderID': 1, 'userid': 1, 'status': 'in transit'}]
        self.assertEqual(res_data, expected_output)

    #test get users route loads the data
    def test_get_users_loads_data(self):
        """
        test loading users data
        """
        response = self.test.get('/api/v1/users')
        res_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'username' in response.data)
        expected_output = [{"userid":1, "username":"Josean", "password":"password", "role":"Admin"}]
        self.assertEqual(res_data, expected_output)

    #test get users route by id loads the data
    def test_get_user_by_id_loads_data(self):
        """
        picking a user with data
        """
        response = self.test.get('/api/v1/users/1')
        res_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        expected_output = [{"userid":1, "username":"Josean", "password":"password", "role":"Admin"}]
        self.assertEqual(res_data, expected_output)
