
from app.utilities.validator import Validator

class DeliveryOrder:
    """ parcel delivery order model structure """
    def __init__(self):
        pass

    def add(self, parcelorders):
        """ adding a parcel delivery order """

        validator = Validator()
        validator.schema([
                            {'key':'destination', 'type':'string', 'min_length':3, 'not_null':True},
                            {'key':'pickupLocation', 'type':'string', 'min_length':3, 'not_null':True},
                            {'key':'parcelSize', 'type':'string', 'min_length':3, 'not_null':True},
                            {'key':'price', 'type':'integer', 'not_null':True},
                            {'key':'status', 'type':'string', 'not_null':True},
                            {'key':'userid', 'type':'integer', 'not_null':True}
                        ])
        result = validator.validate(parcelorders)

        if result['status']:
            self.destination = parcelorders['destination']
            self.pickupLocation = parcelorders['pickupLocation']
            self.parcelSize = parcelorders['parcelSize']
            self.price = parcelorders['price']
            self.status = parcelorders['status']
            self.userid = parcelorders['userid']
            return(True)
        return(result)
        
