
"""
test_parcel_delivery_orders.py File to test parcel order endpoints
"""
import sys
sys.path.append('../')
import unittest
import json
from app import app

class test_parcel_orders(unittest.TestCase):
    """
    test_class
    """

    def setUp(self):
        """
        set up params
        """
        self.test = app.test_client()
        self.parcel = {"orderID":"DO_1", "status":"in transit", "owner":2}

    def tearDown(self):
        """
        tear down params
        """
        self.test = None
        self.parcel = None

    #test index route loads
    def test_index_page_loads(self):
        """
        test index page
        """
        response = self.test.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    #test get parcels route loads
    def test_get_parcels_loads(self):
        """
        test parcels page
        """
        response = self.test.get('/api/v1/parcels', content_type='html/text')
        self.assertEqual(response.status_code, 203)

    #test posting an empty parcel
    def test_post_empty_parcels(self):
        """
        parcels page with empty list
        """
        response = self.test.post('/api/v1/parcels', content_type='html/text')
        self.assertEqual(response.status_code, 203)

    #test get parcel by id
    def test_get_parcel_by_id(self):
        """
        get a parcel by its id
        """
        response = self.test.get('/api/v1/parcels/3', content_type='html/text')
        self.assertEqual(response.status_code, 203)

    #test get parcel by userid
    def test_get_parcel_by_userid(self):
        """
        get parcels by user id
        """
        response = self.test.get('/api/v1/users/4/parcels', content_type='html/text')
        self.assertEqual(response.status_code, 203)

    #test posting with parcel data
    def test_post_data_parcels(self):
        """
        posting parcel data
        """
        res = self.test.post("/api/v1/parcels", headers={"Content-Type": "application/json"}, data=json.dumps(self.parcel))
        res_data = json.loads(res.data)
        expected_output = {"orderID":1, "status":"in transit", "owner":2}
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res_data, expected_output)

    #test cancel parcel
    def test_cancel_parcel(self):
        """
        cancel a parcel
        """
        response = self.test.put('/api/v1/parcels/3/cancel', content_type='html/text')
        self.assertEqual(response.status_code, 203)
