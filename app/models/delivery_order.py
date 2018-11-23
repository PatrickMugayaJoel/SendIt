""" parcel delivery order model structure """

from cerberus import Validator

class DeliveryOrder:
    """ parcel delivery order model structure """
    def __init__(self):
        pass

    def add(self, parcelorders):
        """ adding a parcel delivery order """

        if isinstance(parcelorders['destination'], str) and isinstance(parcelorders['pickupLocation'], str) and isinstance(parcelorders['parcelSize'], str) and isinstance(parcelorders['price'], int) and isinstance(parcelorders['status'], str) and isinstance(parcelorders['userid'], int):
            self.destination = parcelorders['destination']
            self.pickupLocation = parcelorders['pickupLocation']
            self.parcelSize = parcelorders['parcelSize']
            self.price = parcelorders['price']
            self.status = parcelorders['status']
            self.userid = parcelorders['userid']
            return(True)
        return({'msg':"Price must be integer, everything else must be string","status":"failed"})
        
