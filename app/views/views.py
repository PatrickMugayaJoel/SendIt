"""
routes file
"""

from flask import jsonify, request
from app import app
from app.utils.controllers import create_id
parcelorders = []
users = [{"userid":1, "username":"Josean", "password":"password", "role":"Admin"}]

#index route
@app.route('/')
def home():
    """
    home route
    """
    return "Welcome to SendIT.", 200

#get all delivery orders
@app.route('/api/v1/parcels', methods=['GET'])
def deliveryOrders():
    """
    get parcels route
    """
    if parcelorders:
        return jsonify(parcelorders), 200
    return jsonify({"message":"There are no orders to display"}), 404

#post a delivery order
@app.route('/api/v1/parcels', methods=['POST'])
def deliveryOrderspost():
    """
    post parcels route
    """
    data = request.get_json()
    if data:
        user = [item["userid"] for item in users if item["userid"] == data["userid"]]
        if user[0]:
            #generate an id
            data['orderID'] = create_id(parcelorders)
            # appends the delivery orders object to list
            parcelorders.append(data)
            return jsonify(data), 201
    return jsonify({"message":"User id was not found or No data was posted"}), 404

#Get a parcel by ID
@app.route('/api/v1/parcels/<int:orderID>', methods=['GET'])
def deliveryOrder(orderID):
    """
    selecting a parcel by id
    """
    parcel = [item for item in parcelorders if item["orderID"] == orderID]
    if parcel:
        return jsonify(parcel), 200
    return 'Sorry parcel with id: %d not found!'%orderID, 404

#Get a parcels by userID
@app.route('/api/v1/users/<int:userID>/parcels', methods=['GET'])
def parcelOrders(userID):
    """
    selscting parcel by userid
    """
    userparcel = list(filter(lambda parcel: parcel['userid'] == userID, parcelorders))
    if userparcel:
        return jsonify(userparcel), 200
    return 'Sorry user with id: %d not found!'%userID, 404

#Cancel a parcel delivery order
@app.route('/api/v1/parcels/<int:orderID>/cancel', methods=['PUT'])
def parcelOrder(orderID):
    """
    canceling a parcel
    """
    if parcelorders:
        parcel = [item for item in parcelorders if item["orderID"] == orderID]
        if parcel:
            parcel = parcel[0]
            parcel['status'] = 'Canceled'
            return jsonify(parcel), 200
    return 'Sorry parcel order id: %d not found!'%orderID, 404

#post. create a user
@app.route('/api/v1/users', methods=['POST'])
def createuserpost():
    """
    post. create users route
    """
    data = request.get_json()
    if data:
        #generate an id
        data['userid'] = create_id(users)
        # appends user object to list
        users.append(data)
        return jsonify(data), 201
    return jsonify({"message":"No data was posted"}), 404

#get all users
@app.route('/api/v1/users', methods=['GET'])
def getusers():
    """
    get users route
    """
    if users:
        return jsonify(users), 200
    return jsonify({"message":"There are no users to display"}), 404

#Get a user by ID
@app.route('/api/v1/users/<int:userid>', methods=['GET'])
def getuserbyid(userid):
    """
    get a user by id
    """
    user = [item for item in users if item["userid"] == userid]
    if user:
        return jsonify(user), 200
    return 'Sorry user with id: %d not found!'%userid, 404

#Clear all parcels
@app.route('/parcels/cancel', methods=['GET'])
def cancelparcels():
    """
    canceling all parcels
    """
    del parcelorders[:]
    return 'No result',204

#Clear all users
@app.route('/users/cancel', methods=['GET'])
def cancelusers():
    """
    canceling all users
    """
    del users[:]
    return 'No result',204
