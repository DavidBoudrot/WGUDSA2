# David Boudrot
# WGU Data Structures and Algorithms II
# Student ID: 010953326

import csv
import Graph
import Package
import Truck
import hashtable
from SimulationNew import SimulationNew

#O(n)
def create_packages():

    with open('data.csv', 'r') as csvfile:

        reader = csv.reader(csvfile)
        all_packages = []
        packages = hashtable.HashTable(1000)

        for line in reader:
            package = Package.Package(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7])
            # Wrapping the package class into my custom hash table.
            # I did not realize in the rubric that there had to be a package hash table so this is what I came up with.
            i = line[0]
            packages.insert(i, package)
            all_packages.append(package)


        # Above I have created a list of packages to be loaded in the truck from a csv file.
        # The package class is an abstraction for the package data containing all the information about the package


        # Here is going to be the lists of packages that are going to be loaded in the trucks
        # These lists are added to the trucks list to be passed over to the simulation class.

    truck1 = []
    truck2 = []
    truck3 = []

    truck1ints = [15, 16, 34, 40, 2, 4, 1, 6, 20, 13, 14, 31, 37, 29, 19]
    truck2ints = [39, 38, 32, 36, 3, 9, 18, 28, 5]
    truck3ints = [35, 23, 22, 7, 8, 25, 10, 21, 26, 27, 33, 11, 17, 24, 30, 12]

    # I manually load each truck referencing the package id ints above.

    #O(n^2)

    for package in packages:
        if int(package.package_id) in truck1ints:
            truck1.append(package)
        if int(package.package_id) in truck2ints:
            truck2.append(package)
        if int(package.package_id) in truck3ints:
            truck3.append(package)

    # Okay so now we have the packages loaded in the trucks, they just need to be sorted.
    # I will use a nearest neighbor algorithm to find the shortest path between all the packages
    # I have created a class for this.
    # The nearest neighbor algorithm is O(n^2) where n is the number of packages in the truck.

    g = Graph.Graph()
    g.get_distance_matrix()
    packagesForTruck1 = g.nearest_neighbor(truck1)
    truck1Obj = Truck.Truck(1,'08:00', packagesForTruck1)
    packagesForTruck2 = g.nearest_neighbor(truck2)
    truck2Obj = Truck.Truck(2,'09:05', packagesForTruck2)
    packagesForTruck3 = g.nearest_neighbor(truck3)
    truck3Obj = Truck.Truck(3,'9:05', packagesForTruck3)
    truckObjects = [truck1Obj, truck2Obj, truck3Obj]

    #Thats it for our algorithms, now it is time to run the simulation.

    sim = SimulationNew(truckObjects)
    sim.run_simulation()

if __name__ == '__main__':
    create_packages()






