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
from flask_jwt_extended import ( JWTManager, jwt_required, create_access_token, get_jwt_identity)

database = DatabaseConnection()
database.drop_tables()
database.create_tables()
database.default_user()

"""jwt blacklist set"""
blacklist = set()
access_token = None

myuser = User()
if not myuser.add(database.getoneUser(1)):
    pprint('****ERROR**** default user not validated')

#index route
@app.route('/')
def home():
    """ home route """
    return jsonify('wellcome'), 200

#Login route
@app.route('/api/v1/login', methods=['POST'])
def login():
    """login route"""
    if not request.is_json:
        return jsonify({"login2": "Missing JSON data"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    credentials = database.check_user_exists(username.strip(), password.strip())
    
    if not credentials:
        return jsonify({"login3": "Wrong username or password"}), 401

    access_token = create_access_token(identity={'userid':credentials['userid'],'role':credentials['role']})
    return jsonify({'access_token':access_token, 'status':'Successfull'}), 200

#get all delivery orders
@app.route('/api/v1/parcels', methods=['GET'])
@jwt_required
def deliveryOrders():
    """ get parcels route """
    if check_if_token_in_blacklist():
        return jsonify("User logged out"), 401

    userdata=get_jwt_identity()
    if userdata['role'] == 'admin':
        myparcelorders = database.getparcels()
    else:
        myparcelorders = database.getparcelsbyuser(userdata['userid'])
    if myparcelorders:
        return jsonify(myparcelorders), 200
    return jsonify({"message":"There are no orders to display or DB error"}), 400

#post a delivery order
@app.route('/api/v1/parcels', methods=['POST'])
@jwt_required
def deliveryOrderspost():
    """ post parcels route """
    if check_if_token_in_blacklist():
        return jsonify("User logged out"), 401
        
    data = request.get_json()
    if data:
        userdata = get_jwt_identity()
        data['userid'] = userdata['userid']
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
    if check_if_token_in_blacklist():
        return jsonify("User logged out"), 401
        
    parcel = database.getoneparcel(orderID)
    if parcel:
        return jsonify(parcel), 200
    return 'Sorry parcel with id: %d not found!'%orderID, 400

#Get a parcels by userID
@app.route('/api/v1/users/<int:userID>/parcels', methods=['GET'])
@jwt_required
def parcelOrders(userID):
    """ selscting parcel by userid """
    if check_if_token_in_blacklist():
        return jsonify("User logged out"), 401
        
    userparcel = database.getparcelsbyuser(userID)
    if userparcel:
        return jsonify(userparcel), 200
    return 'Sorry user with id: %d not found!'%userID, 400

#Cancel a parcel delivery order
@app.route('/api/v1/parcels/<int:orderID>/cancel', methods=['PUT'])
@jwt_required
def parcelOrder(orderID):
    """ canceling a parcel """
    if check_if_token_in_blacklist():
        return jsonify("User logged out"), 401
        
    parcel = database.getoneparcel(orderID)
    if parcel:
        userdata = get_jwt_identity()
        if not parcel['userid'] == userdata['userid']:
            return jsonify("Update Rights denied!"), 401
        parcel['status'] = 'Cancelled'
        database.update_parcel(parcel)
        return jsonify(parcel), 200
    return 'Sorry parcel order id: %d not found!'%orderID, 400

#post. Signup a user
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
            return jsonify(result), 400

        thisuser = database.getUserbyUsername(data['username'])
        if not thisuser["userid"]:
            return thisuser["msg"]

        return jsonify(thisuser), 201
    return jsonify({"message":"No data was posted"}), 400

#get all users
@app.route('/api/v1/users', methods=['GET'])
@jwt_required
def getusers():
    """ get users route """
    if check_if_token_in_blacklist():
        return jsonify("User logged out"), 401
        
    if not get_jwt_identity()['role'] == 'admin':
        return jsonify('Request denied. You have to be an administrator!'), 401
    listusers = database.getUsers()
    if listusers:
        return jsonify(listusers), 200
    return jsonify({"message":"There are no users to display"}), 400

#Get a user by ID
@app.route('/api/v1/users/<int:userid>', methods=['GET'])
@jwt_required
def getuser_byid(userid):
    """ get a user by id """
    if check_if_token_in_blacklist():
        return jsonify("User logged out"), 401
        
    if not get_jwt_identity()['role'] == 'admin':
        return jsonify('Request denied. You have to be an administrator!'), 401
    user = database.getoneUser(userid)
    try:
        if user['userid']:
            return jsonify(user), 200
        return user['msg'], 400
    except:
            return jsonify({"usrbyid":"User does not exist"}), 400

#Promote user
@app.route('/api/v1/users/<int:userid>/promote', methods=['PUT'])
@jwt_required
def promote(userid):
    """ get a user by id """
    if check_if_token_in_blacklist():
        return jsonify("User logged out"), 401
        
    if not get_jwt_identity()['role'] == 'admin':
        return jsonify('Request denied. You have to be an administrator!'), 401
    user = database.getoneUser(userid)
    try:
        if user['userid']:
            user['role']='admin'
            pprint(database.update_user(user))
            return jsonify(user), 200
        return user['msg'], 400
    except:
            return jsonify({"gtuserbyid":"User does not exist"}), 400

"""Logout"""
@jwt_required
@app.route('/api/v1/logout', methods=['GET'])
def logout():
    """ logout """
    blacklist.add(access_token)
    return jsonify({"login": "Successfully logged out"}), 200

def check_if_token_in_blacklist():
    return access_token in blacklist

"""Clear all parcels"""
@app.route('/parcels/cancel', methods=['GET'])
def cancelparcels():
    """ canceling all parcels """
    return database.truncate('parcels')

"""Clear all users"""
@app.route('/users/cancel', methods=['GET'])
def cancelusers():
    """ canceling all users """
    return database.truncate('users')
