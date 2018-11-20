""" routes file """

from app import app
from app.models.user import User
from flasgger import swag_from
from app.models.delivery_order import DeliveryOrder
from app.utils.serialize import serialize
import datetime
from pprint import pprint
from database import DatabaseConnection
from flask import jsonify, request
from app.utils.controllers import create_id
from flask_jwt_extended import ( JWTManager, jwt_required, create_access_token, get_jwt_identity )

database = DatabaseConnection()
database.drop_tables()
database.create_tables()
database.default_user()

myuser = User()
if not myuser.add(database.getoneUser(1)):
    pprint('****ERROR**** default user not validated')

#index route
@app.route('/')
def home():
    """ home route """
    #current_user = get_jwt_identity()
    #return jsonify(logged_in_as=current_user), 200
    return jsonify('users'), 200

#Login route
@app.route('/api/v1/login', methods=['POST'])
def login():
    """login route"""
    if not request.is_json:
        return jsonify({"msg": "Missing JSON data"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    credentials = database.check_user_exists(username.strip(), password.strip())
    
    if not credentials:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=credentials['userid'])
    return jsonify({'access_token':access_token, 'status':'Successfull'}), 200

#get all delivery orders
@app.route('/api/v1/parcels', methods=['GET'])
@jwt_required
def deliveryOrders():
    """ get parcels route """
    myparcelorders = database.getparcels()
    if myparcelorders:
        return jsonify(myparcelorders), 200
    return jsonify({"message":"There are no orders to display or DB error"}), 400

#post a delivery order
@app.route('/api/v1/parcels', methods=['POST'])
@jwt_required
def deliveryOrderspost():
    """ post parcels route """
    data = request.get_json()
    if data:
        if not database.getoneUser(data["userid"]) == 0:

            newparcel = DeliveryOrder()
            result = newparcel.add(data)
            if not result == True:
                return jsonify(result), 400
            newparcel = serialize(newparcel)

            if not database.insert_data_parcels(newparcel)==True:
                return('database insertion error'),4000

            return jsonify(newparcel), 201
    return jsonify({"message":"User id was not found or No data was posted"}), 400

#Get a parcel by ID
@app.route('/api/v1/parcels/<int:orderID>', methods=['GET'])
@jwt_required
def delivery_Order(orderID):
    """ selecting a parcel by id """
    parcel = database.getoneparcel(orderID)
    if parcel:
        return jsonify(parcel), 200
    return 'Sorry parcel with id: %d not found!'%orderID, 400

#Get a parcels by userID
@app.route('/api/v1/users/<int:userID>/parcels', methods=['GET'])
@jwt_required
def parcelOrders(userID):
    """ selscting parcel by userid """
    userparcel = database.getparcelsbyuser(userID)
    if userparcel:
        return jsonify(userparcel), 200
    return 'Sorry user with id: %d not found!'%userID, 400

#Cancel a parcel delivery order
@app.route('/api/v1/parcels/<int:orderID>/cancel', methods=['PUT'])
@jwt_required
def parcelOrder(orderID):
    """ canceling a parcel """
    parcel = database.getoneparcel(orderID)
    if parcel:
        parcel['status'] = 'Cancelled'
        return jsonify(parcel), 200
    return 'Sorry parcel order id: %d not found!'%orderID, 400

#post. create a user
@app.route('/api/v1/signup', methods=['POST'])
@swag_from('../docs/view/signup.yaml')
def createuserpost():
    """ post. create users route """
    data = request.get_json()
    if data:

        newuser = User()
        thisuser = newuser.add(data)
        if not thisuser == True:
            return jsonify(thisuser), 401
        
        result = database.add_user(newuser)
        if not result == True:
            return jsonify(result), 402

        thisuser = database.getUserbyUsername(data['username'])
        if not thisuser["userid"]:
            return thisuser["msg"]

        return jsonify(thisuser), 201
    return jsonify({"message":"No data was posted"}), 403

#get all users
@app.route('/api/v1/users', methods=['GET'])
@jwt_required
def getusers():
    """ get users route """
    listusers = database.getUsers()
    if listusers:
        return jsonify(listusers), 200
    return jsonify({"message":"There are no users to display"}), 400

#Get a user by ID
@app.route('/api/v1/users/<int:userid>', methods=['GET'])
@jwt_required
def getuser_byid(userid):
    """ get a user by id """
    user = database.getoneUser(userid)
    try:
        if user['userid']:
            return jsonify(user), 200
        return user['msg'], 400
    except:
            return jsonify({"msg":"User does not exist"}), 400

#Clear all parcels
@app.route('/parcels/cancel', methods=['GET'])
def cancelparcels():
    """ canceling all parcels """
    return database.truncate('parcels')
    #return 'No result',204

#Clear all users
@app.route('/users/cancel', methods=['GET'])
def cancelusers():
    """ canceling all users """
    return database.truncate('users')
    #return 'No result',204
