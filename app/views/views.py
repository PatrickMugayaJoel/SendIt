
from flask import jsonify, request
from app.__init__ import app
from app.utils.controllers import create_id
parcelorders = []

#index route
@app.route('/')
def home():
    return "Welcome to SendIT.",200

#get all delivery orders & post a delivery order
@app.route('/api/v1/parcels', methods=['GET','POST'])
def deliveryOrders():
    if request.method == 'GET':

        if parcelorders:
            return jsonify(parcelorders), 200
        return jsonify({"message":"There are no orders to display"}), 203
    if request.method == 'POST':

        data = request.get_json()

        if data:
            #generate an id
            orderID = create_id(parcelorders)

            data['orderID'] = orderID

            # appends the delivery orders object to list
            parcelorders.append(data)
            return jsonify(data), 201
        return jsonify({"message":"No data was posted"}), 203        
    return jsonify({'error': "bad request"}), 400

#Get a parcel by ID
@app.route('/api/v1/parcels/<int:orderID>', methods=['GET'])
def deliveryOrder(orderID):
    if request.method == 'GET':
        parcel = [item for item in parcelorders if item["orderID"] == orderID]
        if parcel:
            return jsonify(parcel), 200
        return 'Sorry parcel id: %d not found!'%orderID, 203
    return jsonify({'error': "bad request"}), 400

#Get a parcels by userID
@app.route('/api/v1/users/<int:userID>/parcels', methods=['GET'])
def parcelOrders(userID):
    if request.method == 'GET':
        userparcel = list(filter(lambda parcel: parcel['owner'] == userID, parcelorders))
        if userparcel:
            return jsonify(userparcel), 200
        return 'Sorry userID id: %d not found!'%userID, 203
    return jsonify({'error': "bad request"}), 400

#Cancel a parcel delivery order
@app.route('/api/v1/parcels/<int:orderID>/cancel', methods=['PUT'])
def parcelOrder(orderID):
    if request.method == 'PUT':
        if parcelorders:
            parcel = next(item for item in parcelorders if item["orderID"] == orderID)
            if parcel:
                parcel['status'] = 'Canceled'
                return jsonify(parcel), 200
            return 'Sorry parcel order id: %d not found!'%orderID, 203
        return 'Sorry No parcel orders found!', 203
    return jsonify({'error': "bad request"}), 400
        