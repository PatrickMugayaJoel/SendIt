from flask import jsonify, abort, request
import datetime
from app.__init__ import app
from app.models.delivery_order import DeliveryOrder
from app.models.user import User
from app.utils.controllers import create_id
parcelorders = []

#index route
@app.route('/')
def home():
    return "Welcome to SendIT."

#get all delivery orders & post a delivery order
@app.route('/api/v1/parcels', methods=['GET','POST'])
def deliveryOrder():
    if request.method == 'GET':

        if parcelorders:
            return jsonify(parcelorders)
        else:
            return jsonify({"message":"There are no orders to display"}), 400
    elif request.method == 'POST':

        data = request.get_json()

        #generate an id
        orderID = create_id(parcelorders)

        data['orderID'] = orderID

        # appends the delivery orders object to list
        parcelorders.append(data)

        return jsonify(data), 201

    else:
        return jsonify({'error': "bad request"}), 404
        