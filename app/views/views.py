""" routes file """

from app import app
from app.models.user import User
from app.utilities.utils import serialize
from app.models.delivery_order import DeliveryOrder
import datetime
from database import DatabaseConnection
from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import ( JWTManager, jwt_required, create_access_token, get_jwt_identity, get_raw_jwt)

database = DatabaseConnection()

if app.env == 'development':
    database.drop_tables()

database.create_tables()
database.default_user()

blacklist = set([item['token'] for item in database.get_blaclist_set()])

jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

#index route
@app.route('/')
def home():
    """ home route """
    return jsonify({"message":'welcome',"status":"success"}), 200

class SignupView(MethodView):
    """users description"""
    #post. Signup a user
    #@app.route('/api/v1/signup', methods=['POST'])
    def Signup(self):
        """ post. create users route """
        data = request.get_json()
        if data:

            newuser = User()
            thisuser = newuser.add(data)
            if not thisuser == True:
                return jsonify(thisuser), 401

            if not database.add_user(newuser) == True:
                return jsonify({"message":"User already exists","status":"failed"}), 400

            thisuser = database.getUserbyUsername(data['username'])
            if not thisuser["userid"]:
                return jsonify({"message":"User not found","status":"failed"}), 404

            return jsonify({"User":thisuser,"status":"success"}), 201
        return jsonify({"message":"No data was posted","status":"failed"}), 400

class LoginView(MethodView):
    #Login route
    #@app.route('/api/v1/login', methods=['POST'])
    def Login(self):
        """login route"""
        if not request.is_json:
            return jsonify({"message":"Missing JSON data","status":"failed"}), 400

        username = request.json.get('username')
        password = request.json.get('password')

        credentials = database.check_user_exists(username.strip(), password.strip())
        
        if not credentials:
            return jsonify({"message": "Wrong username or password","status":"failed"}), 401

        access_token = create_access_token(identity={'userid':credentials['userid'],'role':credentials['role']}, expires_delta=False)
        return jsonify({'access_token':access_token, 'status':'Successfull'}), 200    

class UserView(MethodView):
    #get all users
    #@app.route('/api/v1/users', methods=['GET'])
    @jwt_required
    def Listusers(self):
        """ get users route """
            
        if not get_jwt_identity()['role'] == 'admin':
            return jsonify({"message":'Request denied. You have to be an administrator!',"satus":"failed"}), 401
        listusers = database.getUsers()
        if listusers:
            return jsonify({"users":listusers,"status":"success"}), 200
        return jsonify({"message":"There are no users to display","satus":"failed"}), 400

    #Get a user by ID
    #@app.route('/api/v1/users/<int:userid>', methods=['GET'])
    @jwt_required
    def Getuserbyid(self, userid):
        """ get a user by id """
            
        if not get_jwt_identity()['role'] == 'admin':
            return jsonify({"message":'Request denied. You have to be an administrator!',"satus":"failed"}), 401
        user = database.getoneUser(userid)
        try:
            if user['userid']:
                return jsonify({"user":user,"satus":"success"}), 200
            return user['message'], 400
        except:
                return jsonify({"message":"User does not exist","satus":"failed"}), 400

    #Promote user
    #@app.route('/api/v1/users/<int:userid>/promote', methods=['PUT'])
    @jwt_required
    def Promote(self, userid):
        """ get a user by id """
            
        if not get_jwt_identity()['role'] == 'admin':
            return jsonify({"message":'Request denied. You have to be an administrator!',"satus":"failed"}), 401
        user = database.getoneUser(userid)
        try:
            if user['userid']:
                user['role']='admin'
                print(database.update_user(user))
                return jsonify({"user":user,"satus":"success"}), 200
            return jsonify({"message":"User does not exist","satus":"failed"}), 400
        except:
                return jsonify({"message":"User does not exist error","satus":"failed"}), 400

class LogoutView(MethodView):
    """Logout"""
    #@app.route('/api/v1/logout', methods=['DELETE'])
    @jwt_required
    def Logout(self):
        """ logout """
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        if database.blaclist_a_token(jti) == True:
            return jsonify({"message": "Successfully logged out","satus":"success"}), 200
        return jsonify({"message": "Error logging out","satus":"failed"}), 400

class ParcelView(MethodView):
    #post a delivery order
    #@app.route('/api/v1/parcels', methods=['POST','GET'])
    @jwt_required
    def ParcelDeliveryOrder(self):
        """ post parcels route """

        if request.method == 'POST':
            userdata = get_jwt_identity()
            if userdata["role"]=="admin":
                return jsonify({"message":"Action not allowed for Admins","status":"failed"}), 401
                
            data = request.get_json()
            if data:
                data['userid'] = userdata['userid']
                newparcel = DeliveryOrder()
                result = newparcel.add(data)
                if not result == True:
                    return jsonify(result), 400
                newparcel = serialize(newparcel)

                if not database.insert_data_parcels(newparcel)==True:
                    return jsonify({"message":"Parcel not saved","status":"failed"}),400

                return jsonify({"parcel":newparcel,"status":"success"}), 201
            return jsonify({"message":"No data was posted","status":"failed"}), 400
        
        elif request.method == 'GET':

            userdata=get_jwt_identity()
            if userdata['role'] == 'admin':
                myparcelorders = database.getparcels()
            else:
                myparcelorders = database.getparcelsbyuser(userdata['userid'])
            if myparcelorders:
                return jsonify({"Parcels":myparcelorders,"status":"success"}), 200
            return jsonify({"message":"No parcel orders to display","status":"failed"}), 400
        
        else:
            return jsonify({'message': "bad request","status":"failed"}), 404

    #Get a parcels by userID
    #@app.route('/api/v1/users/<int:userID>/parcels', methods=['GET'])
    @jwt_required
    def UserOrders(self, userID):
        """ selscting parcel by userid """
            
        userparcel = database.getparcelsbyuser(userID)
        if userparcel:
            return jsonify(userparcel), 200
        return jsonify({"message":"Not found!","status":"failed"}), 404

    #Cancel a parcel delivery order
    #@app.route('/api/v1/parcels/<int:orderID>/cancel', methods=['PUT'])
    @jwt_required
    def CancelOrder(self, orderID):
        """ canceling a parcel """
            
        parcel = database.getoneparcel(orderID)
        if parcel:
            userdata = get_jwt_identity()
            if not parcel['userid'] == userdata['userid']:
                return jsonify({"message":"Update Rights denied!","status":"failed"}), 401
            parcel['status'] = 'Cancelled'
            database.update_parcel(orderID,parcel)
            return jsonify({"parcel":parcel,"status":"success"}), 200
        return jsonify({"message":"Parcel Not found!","status":"failed"}), 404

    #Update a parcel delivery order
    #@app.route('/api/v1/parcels/<int:orderID>/update', methods=['PUT'])
    @jwt_required
    def UpdateOrder(self, orderID):
        """ updating a parcel """

        identity = get_jwt_identity()
        parcel = database.getoneparcel(orderID)

        if parcel:
            pass
        else:
            return jsonify({"message":"Parcel not found","status":"failed"}), 404

        if parcel["userid"]==identity["userid"] or identity["role"]=="admin":
            pass
        else:
            return jsonify({"message":"Update Rights denied!","status":"failed"}), 401

        data = request.get_json()

        if data:
            newparcel = DeliveryOrder()
            data['userid']=0
            result = newparcel.add(data)
            if not result == True:
                return jsonify(result), 400

        dbresult = database.update_parcel(parcel["orderid"],newparcel)
        if dbresult==True:
            return jsonify({'message':"Parcel successfuly Updated", "status":"success"}), 200
        return jsonify({'message':dbresult, "status":"failed"}), 400

    #Get a parcel by ID
    #@app.route('/api/v1/parcels/<int:orderID>', methods=['GET'])
    @jwt_required
    def ParcelOrder(self, orderID):
        """ selecting a parcel by id """
            
        parcel = database.getoneparcel(orderID)
        if parcel:
            return jsonify({"parcels":parcel,"status":"success"}), 200
        return jsonify({"message":'Sorry parcel not found!',"status":"failed"}), 404

app.add_url_rule('/api/v1/logout', view_func= LogoutView.as_view('Logout'),
                 methods=["DELETE"])
app.add_url_rule('/api/v1/signup', view_func= SignupView.as_view('Signup'),
                 methods=["POST"])
app.add_url_rule('/api/v1/login', view_func= LoginView.as_view('Login'),
                 methods=["POST"])
app.add_url_rule('/api/v1/users', view_func= UserView.as_view('Listusers'),
                 methods=["GET"])
app.add_url_rule('/api/v1/users/<int:userid>', view_func= UserView.as_view('Getuserbyid'),
                 methods=["GET"])
app.add_url_rule('/api/v1/users/<int:userid>/promote', view_func= UserView.as_view('Promote'),
                 methods=["PUT"])
app.add_url_rule('/api/v1/parcels', view_func= ParcelView.as_view('ParcelDeliveryOrder'),
                 methods=["POST","GET"])
app.add_url_rule('/api/v1/users/<int:userID>/parcels', view_func= ParcelView.as_view('UserOrders'),
                 methods=["GET"])
app.add_url_rule('/api/v1/parcels/<int:orderID>/cancel', view_func= ParcelView.as_view('CancelOrder'),
                 methods=["PUT"])
app.add_url_rule('//api/v1/parcels/<int:orderID>/update', view_func= ParcelView.as_view('UpdateOrder'),
                 methods=["PUT"])
app.add_url_rule('/api/v1/parcels/<int:orderID>', view_func= ParcelView.as_view('ParcelOrder'),
                 methods=["GET"])
