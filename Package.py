class Package:
    def __init__(self, id, address, deadline, city, state, zip, weight, notes):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.deadline = deadline
        self.zip = zip
        self.weight = weight
        self.notes = notes
        self.status = "undelivered"
        self.delivery_time = None
        self.distance = None
