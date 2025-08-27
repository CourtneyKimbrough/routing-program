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
truck_1 = Truck("truck 1")
truck_2 = Truck("truck 2")
truck_3 = Truck("truck 3")
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
    elif note == "Can only be on truck 2":
        load(truck_2, p)
    elif i == 13 or i == 15 or i ==19:
        load(truck_1, p)
    elif note == "Delayed on flight---will not arrive to depot until 9:05 am" or note == "Wrong address listed":
        if p.deadline == "10:30 AM":
            load(truck_3, p)
        else:
            load(truck_2, p)
    




# Parse deadlines 
def parse_deadline(dl):
    if dl == "EOD":
        return datetime.strptime("11:59 PM", "%I:%M %p").time()
    return datetime.strptime(dl, "%I:%M %p").time()

# Load each of the trucks
def load_trucks(truck):
    exit_outer = False
    current_loc = "Hub"
    while not package_hash.isempty() and len(truck.contents) < truck.max_packages: # Check if there are more packages and the truck is not full
        tbl = [p for p in package_hash.update_distances(current_loc, distance_hash)
                if not (p.deadline != "EOD" and truck.name == "truck 2")]
            # Find all of the packages at the nearest address
        for p in tbl: # For every package at the nearest location
            if len(truck.contents) < truck.max_packages: # If there is still room on the truck
                load(truck, p)
                current_loc = p.address
            else:
                exit_outer = True # If the truck is full, stop loading it
                break
        if exit_outer:
            break

load_trucks(truck_3)
load_trucks(truck_1)
load_trucks(truck_2)


def del_time(package, truck):
    speed = truck.speed
    dist = package.distance
    return timedelta(hours=dist/speed)

# Chose the next package based on delivery deadline, then, distance
def choose_next_package(truck, current_addr, distance_hash):
    remaining = truck.contents

    def get_distance(p):
        return distance_hash.distance_lookup(current_addr, p.address)

    # Any package at distance 0
    for p in remaining:
        if get_distance(p) == 0:
            return p

    # Packages with deadlines
    with_deadlines = [p for p in remaining if p.deadline]
    if with_deadlines:
        earliest_deadline = min(parse_deadline(p.deadline) for p in with_deadlines)
        tied = [p for p in with_deadlines if parse_deadline(p.deadline) == earliest_deadline]
        return min(tied, key=get_distance)

    # Pick nearest
    return min(remaining, key=get_distance)

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
        p.truck = truck.name
        truck.mileage += p.distance
        truck.start_time += del_time(p, truck)
        p.status = ["delivered", truck.start_time]
        package_log.insert(p.id, p)
        truck.contents.remove(p)
        current_addr = p.address
    dist = distance_hash.distance_lookup(current_addr, 'Hub')
    truck.start_time += timedelta(hours=dist/18)
    truck.return_time = truck.start_time
    

# Change package status to en route
def en_route_status(truck):
    for p in truck.contents:
        p.status[0] = "en route"
        p.hub_depart = truck.start_time

# Give trucks start times and hub depature times
truck_1.start_time = timedelta(hours=8)
truck_3.start_time = timedelta(hours=9, minutes=5)

# Make deliveries
en_route_status(truck_1)
deliver(truck_1)
en_route_status(truck_3)
deliver(truck_3)
truck_2.start_time = min(truck_1.return_time, truck_3.return_time) # Send out truck 2 when one of the other trucks gets back
en_route_status(truck_2)
deliver(truck_2)

# Function to get total mileage of all trucks
def total_mileage():
    total_mi = 0
    for truck in trucks:
        total_mi += truck.mileage
    return total_mi

def parse_time_string(time_str):
    for fmt in ("%I:%M %p", "%I%p", "%I %p", "%I:%M%p"):
        try:
            return datetime.strptime(time_str, fmt)
        except ValueError:
            continue
    raise ValueError("Invalid time format")

# Function to turn time into time delta
def parse_time_to_timedelta(time_str):
    dt = parse_time_string(time_str)
    return timedelta(hours=dt.hour, minutes=dt.minute)

def get_package_status(pid, cur_time):
    results = package_log.package_lookup(pid)
    cur_time = parse_time_to_timedelta(cur_time)
    if results[-1] == "Delayed on flight---will not arrive to depot until 9:05 am" and cur_time < timedelta(hours=9, minutes =5):
        return (f"\nPackage {pid} is on flight at {cur_time}. It will be delivered to {results[0]} before the {results[1]} deadline on {results[-2]}.")
    elif results[-1] == "Wrong address listed" and cur_time < timedelta(hours=10, minutes =20):
        return (f"\nPackage {pid} is at the hub at {cur_time}. It will be delivered once the correct address is provided, before the {results[1]} deadline on {results[-2]}.")
    elif cur_time < results[-3]:
        return (f"\nPackage {pid} is at the hub at {cur_time}. It will be delivered to {results[0]} before the {results[1]} deadline on {results[-2]}.")
    elif cur_time < results[-4][1]:
        return (f"\nPackage {pid} is en route at {cur_time} to {results[0]} and will be delivered before the {results[1]} deadline on {results[-2]}.")
    else:
        return (f"\nPackage {pid} was delivered at {results[-4][1]} to {results[0]} before the {results[1]} deadline on {results[-2]}.")

def get_valid_time_input(prompt):
    while True:
        time_str = input(prompt)
        try:
            parse_time_string(time_str)
            return time_str
        except ValueError:
            print("Invalid time format. Please enter time as e.g. 10:00 AM, 2AM, or 2:00AM.")

# Function to add color to terminal
def color_text(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def main():
    # CLI Interface
    print("="*50)
    print(color_text("Welcome to the parcel service delivery system!", "96"))
    print("="*50)
    while True:
        choice = input("\nWhat would you like to do?\n1. Check delivery status for a package \n2. Check delivery status for all packages \n3. Check mileage traveled by delivery trucks\n4. Exit\n\n")
        print("")
        match choice:
            case "1":
                while True:
                    try:
                        pid = int(input("Which package would you like to check?\n"))
                        if 1 <= pid <= 40:
                            break
                        else:
                            print("Please enter a package ID between 1 and 40.")
                    except ValueError:
                        print("Please enter a valid number.")
                cur_time = get_valid_time_input("Enter the time you would like to check (e.g. 10:00 AM)\n")
                print(color_text((get_package_status(pid, cur_time)), "92"))
            case "2":
                cur_time = get_valid_time_input("Enter the time you would like to check (e.g. 10:00 AM)\n")
                for p in range(1, 41):
                    print(color_text((get_package_status(p, cur_time)), "92"))
            case "3":
                total = total_mileage()
                print (color_text(f"The total distance travel by all trucks is {total} miles.", "92"))
            case "4":
                print(color_text("Thank you for using the parcel service delivery system!", "92")) 
                break
            case _:
                print("Invalid entry.")

main()