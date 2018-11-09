"""parcel delivery order model structure"""

class DeliveryOrder:
    """parcel delivery order model structure"""
    def __init__(self, orderID, destination, previousCheckpoint, nextCheckpoint, pickupLocation, parcelSize, status, owner, date):
        self.orderID = orderID
        self.destination = destination
        self.previousCheckpoint = previousCheckpoint
        self.nextCheckpoint = nextCheckpoint
        self.pickupLocation = pickupLocation
        self.parcelSize = parcelSize
        self.status = status
        self.owner = owner
        self.date = date
