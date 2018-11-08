"""parcel delivery order model structure"""

class DeliveryOrder:
    """parcel delivery order model structure"""
    def __init__(self, destination, previousCheckpoint, nextCheckpoint, pickupLocation, parcelSize, status, owner, date):
        self.destination = destination
        self.previousCheckpoint = previousCheckpoint
        self.nextCheckpoint = nextCheckpoint
        self.pickupLocation = pickupLocation
        self.parcelSize = parcelSize
        self.status = status
        self.owner = owner
        self.date = date
        
