from flask import jsonify, abort, request
import datetime
from app.__init__ import app
from app.models.delivery_order import DeliveryOrder
from app.models.user import User
parcelorder = []
#index route
@app.route('/')
def home():
    return "Hello"

#get all delivery orders
@app.route('/api/v1/deliveryorders', methods=['GET'])
def deliveryOrder():
    if request.method == 'GET':
        parcel_order = [parcel for parcel in parcelorder]
        if parcel_order:
            return jsonify({"parcel order":parcel_order.__dict__})
        else:
            return jsonify({"message":"There are no orders at this time"}), 400
    else:
        return jsonify({'error': "bad request"}), 404
        