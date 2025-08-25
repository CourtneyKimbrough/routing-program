class Package:
    def __init__(self, id, address, deadline, city, state, zip, weight, notes, status = ["at hub", None]):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.deadline = deadline
        self.zip = zip
        self.weight = weight
        self.notes = notes
        self.status = status
        self.hub_depart = None
        self.distance = None
        self.truck = None