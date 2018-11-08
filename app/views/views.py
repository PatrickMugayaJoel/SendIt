from flask import jsonify, abort, request
import datetime
from app.__init__ import app
from app.models.delivery_order import DeliveryOrder
from app.models.user import User

#index route
@app.route('/')
def home():
    return "Hello"




