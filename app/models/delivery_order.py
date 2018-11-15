"""
parcel delivery order model structure
"""

class DeliveryOrder:
    """
    parcel delivery order model structure
    """
    def __init__(self, parcelorders):
        self.orderID = parcelorders['orderID']
        self.destination = parcelorders['destination']
        self.previousCheckpoint = parcelorders['previousCheckpoint']
        self.nextCheckpoint = parcelorders['nextCheckpoint']
        self.pickupLocation = parcelorders['pickupLocation']
        self.parcelSize = parcelorders['parcelSize']
        self.price = parcelorders['price']
        self.status = parcelorders['status']
        self.userid = parcelorders['userid']
        self.date = parcelorders['date']
