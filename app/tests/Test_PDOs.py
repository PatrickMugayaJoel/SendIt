
"""
test_PDOs.py File to test parcel order endpoints
"""

import unittest
import pytest
import json
import sys
sys.path.append('../')
from app.__init__ import app
from app.views import views

class Test_parcel_orders(unittest.TestCase):
  
    #test cancel a parcel loads the data?
    @pytest.mark.skip()
    def test_cancel_parcel_loads_data(self):
            
        self.test = app.test_client()
        self.parcel = {"orderID":"DO_1","status":"in transit","owner":2}
        self.test.post("/api/v1/parcels",headers={"Content-Type": "application/json"},data=json.dumps(self.parcel))

        response = self.test.put('/api/v1/parcels/1/cancel')
        res_data = json.loads(response.data)
        self.assertEqual(response.status_code,200)
        expected_output = {'orderID': 1, 'status': 'Canceled', 'owner': 2}
        self.assertEqual(res_data, expected_output)
       
    #test get parcels route loads the data
    @pytest.mark.skip()
    def test_get_parcels_loads_data(self):
            
        self.test = app.test_client()
        self.parcel = {"orderID":"DO_1","status":"in transit","owner":2}
        self.test.post("/api/v1/parcels",headers={"Content-Type": "application/json"},data=json.dumps(self.parcel))

        response = self.test.get('/api/v1/parcels')
        res_data = json.loads(response.data)
        self.assertEqual(response.status_code,200)
        expected_output = [{'orderID': 1, 'owner': 2, 'status': 'Canceled'}]
        self.assertEqual(res_data, expected_output)
     
    #test get parcels route by id loads the data
    @pytest.mark.skip()
    def test_get_parcel_by_id_loads_data(self):
            
        self.test = app.test_client()
        self.parcel = {"orderID":"DO_1","status":"in transit","owner":2}
        self.test.post("/api/v1/parcels",headers={"Content-Type": "application/json"},data=json.dumps(self.parcel))

        response = self.test.get('/api/v1/parcels/1')
        res_data = json.loads(response.data)
        self.assertEqual(response.status_code,200)
        expected_output = [{'orderID': 1, 'owner': 2, 'status': 'Canceled'}]
        self.assertEqual(res_data, expected_output)

    #test get parcels route by userid loads the data
    @pytest.mark.skip()
    def test_get_parcel_by_userid_loads_data(self):
            
        self.test = app.test_client()
        self.parcel = {"orderID":"DO_1","status":"in transit","owner":2}
        self.test.post("/api/v1/parcels",headers={"Content-Type": "application/json"},data=json.dumps(self.parcel))

        response = self.test.get('/api/v1/users/2/parcels')
        res_data = json.loads(response.data)
        self.assertEqual(response.status_code,200)
        expected_output = [{'orderID': 1, 'owner': 2, 'status': 'Canceled'}]
        self.assertEqual(res_data, expected_output)

if __name__ == '__main__':
    unittest.main