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

#get all delivery orders
@app.route('/api/v1/parcels', methods=['GET','POST'])
def deliveryOrder():
    if request.method == 'GET':
        
        if parcelorders:
            return jsonify(parcelorders)
        else:
            return jsonify({"message":"There are no orders to display"}), 400
    elif request.method == 'POST':

        data = request.get_json()

        # Get the fields which were sent
        destination = data.get("destination")
        previousCheckpoint = data.get("previousCheckpoint")
        nextCheckpoint = data.get("nextCheckpoint")
        pickupLocation = data.get("pickupLocation")
        parcelSize = data.get("parcelSize")
        status = data.get("status")
        owner = data.get("owner")
        date = datetime.datetime

        orderID = create_id(parcelorders)

        # create a delivery order object
        new_order = DeliveryOrder(orderID=orderID, destination=destination, previousCheckpoint=previousCheckpoint, nextCheckpoint=nextCheckpoint, pickupLocation=pickupLocation, parcelSize=parcelSize, status=status, owner=owner, date=date)

        # appends the delivery orders object to list
        parcelorders.append(new_order)

        return jsonify({
            "message": "Parcel Order successfully created",
            "order": new_order.__dict__
            }), 201

    else:
        return jsonify({'error': "bad request"}), 404
        