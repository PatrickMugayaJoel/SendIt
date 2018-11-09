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
def deliveryOrders():
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

#Get a parcel by ID
@app.route('/api/v1/parcels/<int:orderID>', methods=['GET'])
def deliveryOrder(orderID):
    if request.method == 'GET':
        parcel = [item for item in parcelorders if item["orderID"] == orderID]
        if len(parcel):
            return jsonify(parcel)
        else:
            return 'Sorry parcel id: %d not found!'%orderID
    else:
        return jsonify({'error': "bad request"}), 404

#Get a parcels by userID
@app.route('/api/v1/users/<int:userID>/parcels', methods=['GET'])
def parcelOrders(userID):
    if request.method == 'GET':
        userparcel = list(filter(lambda parcel: parcel['owner'] == userID, parcelorders))
        if len(userparcel):
            return jsonify(userparcel)
        else:
            return 'Sorry userID id: %d not found!'%userID
    else:
        return jsonify({'error': "bad request"}), 404

#Cancel a parcel delivery order
@app.route('/api/v1/parcels/<int:orderID>/cancel', methods=['PUT'])
def parcelOrder(orderID):
    if request.method == 'PUT':
        parcel = next(item for item in parcelorders if item["orderID"] == orderID)
        parcel['status'] = 'Canceled'
        if parcel:
            return jsonify(parcel)
        else:
            return 'Sorry parcel order id: %d not found!'%orderID
    else:
        return jsonify({'error': "bad request"}), 404
        