# Student ID: 012648631

import csv
from datetime import timedelta

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

# Give trucks start times
truck_1.start_time = timedelta(hours=8)
truck_2.start_time = timedelta(hours=8)
truck_3.start_time = timedelta(hours=8)

# Function to load packages
def load(truck, package):
    truck.contents.append(package)
    package_hash.remove(package.id)
    package.status = "loaded"

early = []
semiearly = []
group = []

# Load packages with notes and deadlines:
for i, p in package_hash:
    note = p.notes
    if "Must be delivered with" in note:
        load(truck_1, p)
    elif i == 13 or i == 15 or i ==19:
        load(truck_1, p)
    elif p.deadline == "9:00 AM" or p.deadline == "10:30 AM":
        load(truck_2, p)
    elif note == "Can only be on truck 2":
        load(truck_2, p)
    elif note == "Delayed on flight---will not arrive to depot until 9:05 am" or note == "Wrong address listed":
        load(truck_3, p)

# Load each of the trucks
for truck in trucks:
    exit_outer = False
    current_loc = "Hub"
    while not package_hash.isempty() and len(truck.contents) < truck.max_packages: # Check if there are more packages and the truck is not full
        tbl = package_hash.update_distances(current_loc, distance_hash) # Find all of the packages at the nearest address
        for p in tbl: # For every package at the nearest location
            if len(truck.contents) < truck.max_packages: # If there is still room on the truck
                load(truck, p)
                current_loc = p.address
            else:
                exit_outer = True # If the truck is full, stop loading it
                break
        if exit_outer:
            break
    print("truck")
    for p in truck.contents:
        print(p.id)

def del_time(package, truck):
    speed = truck.speed
    dist = package.distance
    return timedelta(hours=dist/speed)

# Deliver packages
for truck in trucks:
    current_addr = "Hub"
    for p in truck.contents:
        p.distance = distance_hash.distance_lookup(current_addr, p.address)
        truck.start_time += del_time(p, truck)
        p.delivery_time = truck.start_time
        print (p.id)
        print (p.delivery_time)
        current_addr = p.address






'''

#for p in package_hash:
    #print(p)
for from_loc, inner_hash in distance_hash:
    print(from_loc)  # HUB, 1060 Dalton Ave S, etc.
    for to_loc, dist in inner_hash:  # dist is a string
        print(f"{to_loc}: {dist}")

#print (distance_hash.distance_lookup("3575 W Valley Central Station bus Loop","2600 Taylorsville Blvd"))
'''