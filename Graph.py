import csv
import heapq
import itertools
from hashtable import HashTable

class Graph:
    def __init__(self):
        # Initialize the class with empty lists and dictionaries
        self.address_table = {}
        self.addresses = []
        self.distances = []
        self.list_of_dist = []
        self.hash_table = HashTable(1000)


    # Get the distance matrix from a CSV file and store it as a list
    # O(n) where n is the number of rows in the CSV file
    def get_distance_matrix(self):
        with open('distance.csv', 'r') as csvfile:
            distancedata = csv.reader(csvfile)
            list_of_dist = list(distancedata)
            self.list_of_dist = list_of_dist

        address_table = {}

        # Open the CSV file containing addresses and read its contents
        with open('addresses.csv', 'r') as csvfile:
            addressdata = csv.reader(csvfile)
            addresses = []
            for line in addressdata:
                address_table[line[1]] = int(line[0])
                addresses.append(line[1])
                self.hash_table.insert(line[1], int(line[0]))
        self.address_table = address_table


    # Get the distance between two addresses
    # O(1)
    def get_distance(self, address1, address2):
        package1Index = self.hash_table.lookup(address1)
        package2Index = self.hash_table.lookup(address2)
        return float(self.list_of_dist[package1Index][package2Index])

    # Find the nearest neighbor path through all packages
    # O(n^2) where n is the number of packages
    def nearest_neighbor(self, packages):

        # Create an empty list to store the final path
        finalpath = []
        import Package
        # Create a starting package representing the hub
        hub = Package.Package("0", "4001 South 700 East", "Salt Lake City", "UT", "84111", "9:00 AM", "16", "Hub")
        # Create a copy of the packages list to reference later
        packagesclone = packages.copy()
        # Initialize a variable to keep track of the total distance traveled
        total = 0
        total = 0
        # Iterate through the packages list until every package has been added to the final path
        while len(finalpath) != len(packagesclone) + 1:
            if len(finalpath) == 0:
                finalpath.append(hub)
            else:
                min = float('inf')
                for package in packages:
                    # Calculate the distance between the last package added to the path and each remaining package
                    distance = self.get_distance(finalpath[-1].address, package.address)
                    if package.deadline == "EOD":
                        # If the package has an EOD deadline, triple the distance traveled to it
                        distance = distance * 3
                    if distance < min:
                        min = distance
                        minpackage = package
                # Add the package with the shortest distance to the path and update the total distance traveled
                finalpath.append(minpackage)
                if minpackage.deadline == "EOD":
                    total += (min / 3)
                else:
                    total += min
                print("total distance: " + str(total) + " + " + str(min) + " = " + str(total + min))
                # Remove the package from the packages list
                packages.remove(minpackage)

        return finalpath