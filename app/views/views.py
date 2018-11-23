""" routes file """

from app import app
from app.models.user import User
from flasgger import swag_from
from app.models.delivery_order import DeliveryOrder
import datetime
from database import DatabaseConnection
from flask import jsonify, request
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
    print('****ERROR**** default user not validated')

#index route
@app.route('/')
def home():
    """ home route """
    return jsonify({"msg":'welcome',"status":"success"}), 200

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

        if not database.add_user(newuser) == True:
            return jsonify({"msg":"User already exists","status":"failed"}), 400

        thisuser = database.getUserbyUsername(data['username'])
        if not thisuser["userid"]:
            return jsonify({"msg":"User not found","status":"failed"}), 400

        return jsonify({"User":thisuser,"status":"success"}), 201
    return jsonify({"msg":"No data was posted","status":"failed"}), 400

#Login route
@app.route('/api/v1/login', methods=['POST'])
def login():
    """login route"""
    if not request.is_json:
        return jsonify({"msg":"Missing JSON data","status":"failed"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    credentials = database.check_user_exists(username.strip(), password.strip())
    
    if not credentials:
        return jsonify({"msg": "Wrong username or password","status":"failed"}), 401

    access_token = create_access_token(identity={'userid':credentials['userid'],'role':credentials['role']}, expires_delta=False)
    return jsonify({'access_token':access_token, 'status':'Successfull'}), 200

#post a delivery order
@app.route('/api/v1/parcels', methods=['POST'])
@jwt_required
def deliveryOrderspost():
    """ post parcels route """
    if check_if_token_in_blacklist():
        return jsonify({"msg":"User logged out","status":"failed"}), 401
    
    userdata = get_jwt_identity()
    if userdata["role"]=="admin":
        return jsonify({"msg":"Action not allowed for Admins","status":"failed"}), 401
        
    data = request.get_json()
    if data:
        data['userid'] = userdata['userid']
        newparcel = DeliveryOrder()
        result = newparcel.add(data)
        if not result == True:
            return jsonify(result), 400
        newparcel = serialize(newparcel)

        if not database.insert_data_parcels(newparcel)==True:
            return jsonify({"msg":"Parcel not saved","status":"failed"}),400

        return jsonify({"parcel":newparcel,"status":"success"}), 201
    return jsonify({"msg":"No data was posted","satatus":"failed"}), 400

#get all delivery orders
@app.route('/api/v1/parcels', methods=['GET'])
@jwt_required
def deliveryOrders():
    """ get parcels route """
    if check_if_token_in_blacklist():
        return jsonify({"msg":"User logged out","status":"failed"}), 401

    userdata=get_jwt_identity()
    if userdata['role'] == 'admin':
        myparcelorders = database.getparcels()
    else:
        myparcelorders = database.getparcelsbyuser(userdata['userid'])
    if myparcelorders:
        return jsonify({"Parcels":myparcelorders,"status":"success"}), 200
    return jsonify({"msg":"No parcel orders to display","status":"failed"}), 400

#Get a parcel by ID
@app.route('/api/v1/parcels/<int:orderID>', methods=['GET'])
@jwt_required
def delivery_Order(orderID):
    """ selecting a parcel by id """
    if check_if_token_in_blacklist():
        return jsonify({"msg":"User logged out","status":"failed"}), 401
        
    parcel = database.getoneparcel(orderID)
    if parcel:
        return jsonify({"parcels":parcel,"status":"success"}), 200
    return jsonify({"msg":'Sorry parcel found!',"status":"failed"}), 400

#Get a parcels by userID
@app.route('/api/v1/users/<int:userID>/parcels', methods=['GET'])
@jwt_required
def parcelOrders(userID):
    """ selscting parcel by userid """
    if check_if_token_in_blacklist():
        return jsonify({"msg":"User logged out","status":"failed"}), 401
        
    userparcel = database.getparcelsbyuser(userID)
    if userparcel:
        return jsonify(userparcel), 200
    return jsonify({"msg":"Not found!","status":"failed"}), 400

#Cancel a parcel delivery order
@app.route('/api/v1/parcels/<int:orderID>/cancel', methods=['PUT'])
@jwt_required
def parcelOrder(orderID):
    """ canceling a parcel """
    if check_if_token_in_blacklist():
        return jsonify({"msg":"User logged out","status":"failed"}), 401
        
    parcel = database.getoneparcel(orderID)
    if parcel:
        userdata = get_jwt_identity()
        if not parcel['userid'] == userdata['userid']:
            return jsonify({"msg":"Update Rights denied!","status":"failed"}), 401
        parcel['status'] = 'Cancelled'
        database.update_parcel(orderID,parcel)
        return jsonify({"parcel":parcel,"status":"success"}), 200
    return jsonify({"msg":"Parcel Not found!","status":"failed"}), 400

#Update a parcel delivery order
@app.route('/api/v1/parcels/<int:orderID>/update', methods=['PUT'])
@jwt_required
def updateparcelOrder(orderID):
    """ updating a parcel """
    if check_if_token_in_blacklist():
        return jsonify({"msg":"User logged out","status":"failed"}), 401

    identity = get_jwt_identity()
    parcel = database.getoneparcel(orderID)

    if parcel:
        pass
    else:
        return jsonify({"msg":"Parcel not found","status":"failed"}), 400

    if parcel["userid"]==identity["userid"] or identity["role"]=="admin":
        pass
    else:
        return jsonify({"msg":"Update Rights denied!","status":"failed"}), 401

    data = request.get_json()

    if data:
        newparcel = DeliveryOrder()
        data['userid']=0
        result = newparcel.add(data)
        if not result == True:
            return jsonify(result), 400

    dbresult = database.update_parcel(parcel["orderid"],newparcel)
    if dbresult==True:
        return jsonify({'msg':"Parcel successfuly Updated", "status":"success"}), 200
    return jsonify({'msg':dbresult, "status":"failed"}), 400

#get all users
@app.route('/api/v1/users', methods=['GET'])
@jwt_required
def getusers():
    """ get users route """
    if check_if_token_in_blacklist():
        return jsonify({"msg":"User logged out","status":"failed"}), 401
        
    if not get_jwt_identity()['role'] == 'admin':
        return jsonify({"msg":'Request denied. You have to be an administrator!',"satus":"failed"}), 401
    listusers = database.getUsers()
    if listusers:
        return jsonify(listusers), 200
    return jsonify({"msg":"There are no users to display","satus":"failed"}), 400

#Get a user by ID
@app.route('/api/v1/users/<int:userid>', methods=['GET'])
@jwt_required
def getuser_byid(userid):
    """ get a user by id """
    if check_if_token_in_blacklist():
        return jsonify({"msg":"User logged out","status":"failed"}), 401
        
    if not get_jwt_identity()['role'] == 'admin':
        return jsonify({"msg":'Request denied. You have to be an administrator!',"satus":"failed"}), 401
    user = database.getoneUser(userid)
    try:
        if user['userid']:
            return jsonify({"user":user,"satus":"success"}), 200
        return user['msg'], 400
    except:
            return jsonify({"msg":"User does not exist","satus":"failed"}), 400

#Promote user
@app.route('/api/v1/users/<int:userid>/promote', methods=['PUT'])
@jwt_required
def promote(userid):
    """ get a user by id """
    if check_if_token_in_blacklist():
        return jsonify({"msg":"User logged out","status":"failed"}), 401
        
    if not get_jwt_identity()['role'] == 'admin':
        return jsonify({"msg":'Request denied. You have to be an administrator!',"satus":"failed"}), 401
    user = database.getoneUser(userid)
    try:
        if user['userid']:
            user['role']='admin'
            print(database.update_user(user))
            return jsonify({"user":user,"satus":"success"}), 200
        return jsonify({"msg":"User does not exist","satus":"failed"}), 400
    except:
            return jsonify({"msg":"User does not exist error","satus":"failed"}), 400

"""Logout"""
@jwt_required
@app.route('/api/v1/logout', methods=['GET'])
def logout():
    """ logout """
    blacklist.add(access_token)
    return jsonify({"login": "Successfully logged out"}), 200

def check_if_token_in_blacklist():
    return access_token in blacklist

def serialize(objt):
    return objt.__dict__

def serialize_list(mylist):
    listtwo = []
    for item in mylist:
        listtwo.append(serialize(item))
    return listtwo
