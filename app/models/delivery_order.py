""" parcel delivery order model structure """

from cerberus import Validator

class DeliveryOrder:
    """ parcel delivery order model structure """
    def __init__(self):
        pass

    def add(self, parcelorders):
        """ adding a parcel delivery order """

        schema = {'orderID': {'type': 'integer'}, 'destination': {'type': 'string'},
                    'pickupLocation': {'type': 'string'}, 'parcelSize': {'type': 'string'},
                     'price': {'type': 'string'}, 'status': {'type': 'string'},
                      'userid': {'type': 'integer'}, 'date': {'type': 'string'}}

        v = Validator(schema)
        v.allow_unknown = True

        if v.validate(parcelorders, schema):
            self.orderID = parcelorders['orderID']
            self.destination = parcelorders['destination']
            self.pickupLocation = parcelorders['pickupLocation']
            self.parcelSize = parcelorders['parcelSize']
            self.price = parcelorders['price']
            self.status = parcelorders['status']
            self.userid = parcelorders['userid']
            self.date = parcelorders['date']
            return(True)
        return(v.errors)
