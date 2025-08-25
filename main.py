# Student ID: 012648631

import csv

from HashTable import HashTable
from Package import Package
from Truck import Truck

# Function to read package info from package.csv and turn it into a hash map
def load_packages(file):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        rows = list(reader)  # store all rows in memory
        row_count = len(rows)
        
        package_hash = HashTable(row_count)
        
        for row in rows:
            id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zip = row[4]
            deadline = row[5]
            weight = row[6]
            notes = row[7]
            my_package = Package(id, address, deadline, city, state, zip, weight, notes)
            package_hash.insert(id, my_package)
    return package_hash

# Function to read distance matrix and turn it into a hash map
def load_distances(file):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)[1:]
        distance_hash = HashTable(len(header))
        for row in reader:
            from_loc = row[0]
            temp_hash = HashTable(len(header))
            for i, to_loc in enumerate(header):
                temp_hash.insert(to_loc, float(row[i + 1]))
            distance_hash.insert(from_loc, temp_hash)
    return distance_hash


# Create hash table of packages:
package_hash = load_packages('package.csv')

# Create hash table of distances:
distance_hash = load_distances('distances.csv')

# Create 3 truck objects and add them to an array
truck_1 = Truck()
truck_2 = Truck()
truck_3 = Truck()
trucks = [truck_1, truck_2, truck_3]



for truck in trucks:
    current_loc = "Hub"
    while not package_hash.isempty() and len(truck.contents) < truck.max_packages:
        tbl = package_hash.update_distances(current_loc, distance_hash)
        for p in tbl:
            truck.contents.append(p)
            package_hash.remove(p)
'''





#for p in package_hash:
    #print(p)
for from_loc, inner_hash in distance_hash:
    print(from_loc)  # HUB, 1060 Dalton Ave S, etc.
    for to_loc, dist in inner_hash:  # dist is a string
        print(f"{to_loc}: {dist}")

#print (distance_hash.distance_lookup("3575 W Valley Central Station bus Loop","2600 Taylorsville Blvd"))
'''