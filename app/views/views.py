"""
routes file
"""

from app import app
from app.models.user import User
from app.models.delivery_order import DeliveryOrder
from app.utils.serialize import serialize
from flask import jsonify, request
from app.utils.controllers import create_id
from flask_jwt_extended import ( JWTManager, jwt_required, create_access_token, get_jwt_identity )
parcelorders = []
users = []

myuser = User()
myuser.add({"userid":1, "name":"admin", "username":"admin", "password":"admin", "role":"Admin"})
users.append(serialize(myuser))

#index route
@app.route('/')
def home():
    """
    home route
    """
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

#Login route
@app.route('/api/v1/login', methods=['POST'])
def login():
    """
    login route
    """
    if not request.is_json:
        return jsonify({"msg": "Missing JSON data"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    credentials = list(filter(lambda user: user['username'] == username and user['password'] == password, users))
    
    if not credentials:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

#get all delivery orders
@app.route('/api/v1/parcels', methods=['GET'])
@jwt_required
def deliveryOrders():
    """
    get parcels route
    """
    if parcelorders:
        return jsonify(parcelorders), 200
    return jsonify({"message":"There are no orders to display"}), 400

#post a delivery order
@app.route('/api/v1/parcels', methods=['POST'])
@jwt_required
def deliveryOrderspost():
    """
    post parcels route
    """
    data = request.get_json()
    if data:
        user = next((item["userid"] for item in users if item["userid"] == data["userid"]), None)
        if user:
            #generate an id
            data['orderID'] = create_id(parcelorders)

            newparcel = DeliveryOrder()
            if not newparcel.add(data):
                return jsonify({"message":"Invalid data"}), 400
            newparcel = serialize(newparcel)

            # appends the delivery orders object to list
            parcelorders.append(newparcel)
            return jsonify(newparcel), 201
    return jsonify({"message":"User id was not found or No data was posted"}), 400

#Get a parcel by ID
@app.route('/api/v1/parcels/<int:orderID>', methods=['GET'])
@jwt_required
def delivery_Order(orderID):
    """
    selecting a parcel by id
    """
    parcel = [item for item in parcelorders if item["orderID"] == orderID]
    if parcel:
        return jsonify(parcel), 200
    return 'Sorry parcel with id: %d not found!'%orderID, 400

#Get a parcels by userID
@app.route('/api/v1/users/<int:userID>/parcels', methods=['GET'])
@jwt_required
def parcelOrders(userID):
    """
    selscting parcel by userid
    """
    userparcel = list(filter(lambda parcel: parcel['userid'] == userID, parcelorders))
    if userparcel:
        return jsonify(userparcel), 200
    return 'Sorry user with id: %d not found!'%userID, 400

#Cancel a parcel delivery order
@app.route('/api/v1/parcels/<int:orderID>/cancel', methods=['PUT'])
@jwt_required
def parcelOrder(orderID):
    """
    canceling a parcel
    """
    if parcelorders:
        parcel = [item for item in parcelorders if item["orderID"] == orderID]
        if parcel:
            parcel = parcel[0]
            parcel['status'] = 'Cancelled'
            return jsonify(parcel), 200
    return 'Sorry parcel order id: %d not found!'%orderID, 400

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

        newuser = User()
        if not newuser.add(data):
            return jsonify({"message":"Invalid data"}), 400
        newuser = serialize(newuser)

        # appends user object to list
        users.append(newuser)
        return jsonify(data), 201
    return jsonify({"message":"No data was posted"}), 400

#get all users
@app.route('/api/v1/users', methods=['GET'])
#@jwt_required
def getusers():
    """
    get users route
    """
    if users:
        return jsonify(users), 200
    return jsonify({"message":"There are no users to display"}), 400

#Get a user by ID
@app.route('/api/v1/users/<int:userid>', methods=['GET'])
@jwt_required
def getuser_byid(userid):
    """
    get a user by id
    """
    user = [item for item in users if item["userid"] == userid]
    if user:
        return jsonify(user), 200
    return 'Sorry user with id: %d not found!'%userid, 400

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
