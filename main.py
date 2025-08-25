# Student ID: 012648631

import csv
from datetime import timedelta, datetime

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

# Create empty package log hash
package_log = HashTable(40)

# Create 3 truck objects and add them to an array
truck_1 = Truck("truck_1")
truck_2 = Truck("truck_2")
truck_3 = Truck("truck_3")
trucks = [truck_1, truck_2, truck_3]

# Function to load packages
def load(truck, package):
    truck.contents.append(package)
    package_hash.remove(package.id)
    package.truck = truck.name


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

# Parse deadlines 
def parse_deadline(dl):
    if dl == "EOD":
        return datetime.strptime("11:59 PM", "%I:%M %p").time()
    return datetime.strptime(dl, "%I:%M %p").time()

# Sort packages on Truck 2 by deadline
truck_2.contents.sort(key=lambda p: parse_deadline(p.deadline))

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

# Chose the next package based on delivery deadline, then, distance
def choose_next_package(truck, current_addr, distance_hash):
    remaining = truck.contents
    urgent = [p for p in remaining if parse_deadline(p.deadline) <= datetime.strptime("10:30 AM", "%I:%M %p").time()]
    if urgent:
        return min(urgent, key=lambda p: parse_deadline(p.deadline)) # Pick the one with the earliest deadline
    else:
        return min(remaining, key=lambda p: distance_hash.distance_lookup(current_addr, p.address)) # Otherwise pick nearest neighbor

# Deliver packages
def deliver(truck):
    current_addr = "Hub"

    if truck.start_time >= timedelta(hours=10, minutes=20):
        for p in truck.contents: 
            if p.id == 9:  # package with delayed address update
                p.address = "410 S State St"

    while len(truck.contents) > 0:
        p = choose_next_package(truck, current_addr, distance_hash)
        p.distance = distance_hash.distance_lookup(current_addr, p.address)
        truck.start_time += del_time(p, truck)
        p.status[1] = truck.start_time
        p.status[0] = "delivered"
        package_log.insert(p.id, p)
        truck.contents.remove(p)
        print(p.id, p.status[1])
        current_addr = p.address
    dist = distance_hash.distance_lookup(current_addr, 'Hub')
    truck.start_time += timedelta(hours=dist/18)
    truck.return_time = truck.start_time
    print("return time", truck.return_time)

# Change package status to en route
def en_route_status(truck):
    for p in truck.contents:
        p.status[0] = "en route"
        p.hub_depart = truck.start_time



# Give trucks start times and hub depature times
truck_1.start_time = timedelta(hours=8)
truck_2.start_time = timedelta(hours=8)


en_route_status(truck_1)
deliver(truck_1)
en_route_status(truck_2)
deliver(truck_2)
truck_3.start_time = min(truck_1.return_time, truck_2.return_time) # Send out truck 3 when one of the other trucks gets back
en_route_status(truck_3)
deliver(truck_3)

def get_package_status(pid, cur_time):
    results = package_log.package_lookup(pid)
    if cur_time < results[-1]:
        return (f"Package {p.id} is at the hub at {cur_time}")
    elif cur_time < results[-2][1]:
        return (f"Package {p.id} is en route at {cur_time}")
    else:
        (f"Package {p.id} was delivered at {results[-2][1]}")

# CLI Interface
print ("Welcome to the parcel service delivery system!")
choice = input("What would you like to do? \n 1. Check delivery status for a package \n 2. Check delivery status for all packages 3. Check mileage traveled by delivery trucks")

match choice:
    case "1":
        pid = int(input("Which package would you like to check?"))
        cur_time = input("Enter the time you would like to check")
        print(get_package_status(pid, cur_time))
    #case 2:
    #case 3:
    #case _:
