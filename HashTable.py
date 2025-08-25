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

    def package_lookup(self, key):
        index = self.hash_function(key)
        for k, v in self.table[index]:
            if k == key:
                return v.address, v.deadline, v.city, v.zip, v.weight, v.status
        return None
    
    def distance_lookup(self, key, key2):
        index = self.hash_function(key)
        for k, v in self.table[index]:
            if k == key:
                inner_ind = v.hash_function(key2)
                for inner_k, inner_v in v.table[inner_ind]:
                    if inner_k == key2:
                        return inner_v
        return None
    
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