class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range (size)]

    # Function to convert key into an index in table
    def hash_function(self, key):
        if isinstance(key, int):
            return key % self.size
        return sum(ord(c) for c in key) % self.size # string-to-int conversion
    
    def insert(self, key, value):
        index = self.hash_function(key)
        self.table[index].append((key, value))

    # Look up function that takes package ID and returns data
    def package_lookup(self, key):
        index = self.hash_function(key)
        for k, v in self.table[index]:
            if k == key:
                return v.address, v.deadline, v.city, v.zip, v.weight, v.status, v.hub_depart
        return None
    
    def distance_lookup(self, key, key2):
        key = key.strip()
        key2 = key2.strip()
        for from_loc, inner_hash in self:
            for to_loc, dist in inner_hash:  # dist is a string
                if from_loc == key and to_loc == key2:
                    return float(dist)
        print("not found")
    
    def remove(self, key):
        index = self.hash_function(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                return True
        return False
    
    # Function to iterate through hash table
    def __iter__(self):
        for section in self.table:
            for k, v in section:
                yield k, v

    # Function to check if hash table is empty
    def isempty(self):
        for p in self.table:
            if p != []:
                return False
        return True
    
    # Function to update distance on each package
    def update_distances(self, current_loc, distance_hash):
        mini = 15
        load = []
        for i, p in self:
            p.distance = distance_hash.distance_lookup(current_loc, p.address)
            if p.distance < mini:
                mini = p.distance
                load.append(p)
            elif p.distance == mini:
                load.append(p)
        return load