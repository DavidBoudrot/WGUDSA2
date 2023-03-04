import csv
import heapq
import itertools
import hashtable

class Graph:

    def __init__(self):
        self.address_table = {}
        self.addresses = []
        self.distances = []
        self.list_of_dist = []

    def get_distance_matrix(self):

        with open('distance.csv', 'r') as csvfile:
            distancedata = csv.reader(csvfile)
            list_of_dist = list(distancedata)
            self.list_of_dist = list_of_dist

        address_table = {}
        # This will create a dictionary that will have the address as the key and the index of the address as the value.
        with open('addresses.csv', 'r') as csvfile:
            addressdata = csv.reader(csvfile)
            addresses = []
            for line in addressdata:
                address_table[line[1]] = int(line[0])
                addresses.append(line[1])
                # dict = {'123 Street st' : 0}
                # addreses = ['123 Street st', ...]
        self.address_table = address_table


    def get_distance(self, address1, address2):
        #Convert the addresses to indexes with the address table


        package1Index = int(self.address_table[address1])
        package2Index = int(self.address_table[address2])

        return float(self.list_of_dist[package1Index][package2Index])




    def nearest_neighbor(self, packages):
        clone = packages.copy()
        #I am going to do this algorithm starting with every package with a deadline of EOD
        #Then I will pick the best option.
        path = []
        for package in packages:
            if package.deadline == "EOD":
                path.append(package)
        if len(path) == 0:
            path.append(packages[0])

        deadline_count = sum(1 for package in packages if package.deadline != "EOD")
        paths = []
        for package in path:
            finalpath = [package]
            total_distance = 0
            packages = clone.copy()
            while len(finalpath) < len(clone):
                minimum = float('inf')
                prev = path[-1]
                cheapest_package = None
                for package in packages:
                    if package not in finalpath and minimum > self.get_distance(prev.address, package.address):
                        if package.deadline != 'EOD' or len(finalpath) >= deadline_count:
                            cheapest_package = package
                            minimum = self.get_distance(prev.address, package.address)
                if cheapest_package is not None:
                    total_distance += minimum
                    finalpath.append(cheapest_package)
                    packages.remove(cheapest_package)
                else:
                    break
            #add packages back to the list

            paths.append([finalpath, total_distance])

        minimum = float('inf')
        for path in paths:
            print(path[1])
            if path[1] < minimum:

                minimum = path[1]
                finalpath = path[0]

        print("Final Path: ")
        print("Total Distance: " + str(minimum))
        return finalpath













