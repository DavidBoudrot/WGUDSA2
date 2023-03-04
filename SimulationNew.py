import heapq
from datetime import datetime, timedelta
class SimulationNew:
    trucks = []

    #To start the simulation, I have to pass the trucks into this class.
    def __init__(self, trucks):
        self.all_packages = []
        self.trucks = trucks

    #Here is how running the sim works.
    #First I get the path for each truck.
    #Then I loop through each package, I make note of the time it was delivered by using the get_distance method in the package class.
    #get_distance is called with the previous package and the current package.
    #The time is then added to the package object.
    #Then we will be left with a list of packages and times.
    #We sort by time and "deliver" the packages by popping them and changing the package status to delivered.
    #If at any time the user wants to see the status of the packages, they can call the get_status method by entering "i"

    #O(n)
    def run_simulation(self):

        truck1 = self.trucks[0]
        truck2 = self.trucks[1]
        truck3 = self.trucks[2]
        truck1Path = truck1.get_current_packages()
        truck2Path = truck2.get_current_packages()
        truck3Path = truck3.get_current_packages()
        print("Paths for trucks 1, 2, and 3 calculated.")

    # Calling the deliver method for each package in the path.
    # It should be noted that the deliver method is not actually delivering the package to the user or changing the package,
    # it is just adding the time to the package object.
    # The package is actually delivered to the user in the for loop below.

        print(truck1.get_current_packages())
        # O(n)
        for package in truck1Path:
            if package.package_id == '0':
                print("Starting at hub")
                continue
            else:
                self.deliver(package, truck1)
        # O(n)
        for package in truck3Path:
            if package.package_id == '0':
                print("Starting at hub")
                continue
            else:
                self.deliver(package, truck3)


        # O(n)
        truck2.time = truck3.time
        for package in truck2Path:
            if package.package_id == '0':
                print("Starting at hub")
                continue
            else:
                self.deliver(package, truck2)



    # At this point we have a list of packages with their delivery times.
    # All that needs to be done is pop them off the list, update the status and print them out.

        print("Truck1 mileage is " + str(truck1.distance))
        print("Truck2 mileage is " + str(truck2.distance))
        print("Truck3 mileage is " + str(truck3.distance))

        print('Times for deliveries are as follows:')
        truck1enroute = False
        truck2enroute = False
        truck3enroute = False

        # O(n)
        # Sorting the packages by delivery time.
        self.all_packages.sort(key=lambda x: x.delivered_time)


        for package in self.all_packages:

        # If the user wants to see the status of the packages, they can enter "i" at any time.
            i = input("Press Enter to continue or enter I for stats...")
            if i == "i":
                self.lookupStats()
            print(package.package_id + ' delivered at ' + str(package.delivered_time) + ' by truck ' + str(package.truck_id)
                  + ' with a deadline of ' + package.deadline + ' and a special note of ' + package.special_notes)
            package.delivery_status = "Delivered"
            package.delivered = True

        # I set the trucks to enroute when the first package is delivered.

            if str(package.truck_id) == str('1') and truck1enroute == False:
                for package in truck1Path:
                   package.delivery_status = "En route"
                truck1enroute = True

            if str(package.truck_id) == str('2') and truck2enroute == False:
                for package in truck2Path:
                    package.delivery_status = "En route"
                truck2enroute = True

            if str(package.truck_id) == str('3') and truck3enroute == False:
                for package in truck3Path:
                    package.delivery_status = "En route"
                truck3enroute = True


        print("Total Miles Traveled: " + str(int(truck1.distance + truck2.distance + truck3.distance)))

    #This method is called by the run_simulation method.
    #It determines if the package is the first package to be delivered.
    #If it is, it will calculate the distance from the hub to the package.
    #If it is not, it will calculate the distance from the previous package to the current package.

    #O(1)
    def deliver(self, package, truck):
        package.delivered_time = truck.time
        package.truck_id = truck.truck_id
        if truck.last_package == None:
            truck.last_package = package
            distance = 0
            self.increment_truck_time(distance, truck)
        else:
            distance = package.get_distance(truck.last_package)
            self.increment_truck_time(distance, truck)
            truck.last_package = package

        self.all_packages.append(package)
        print(truck.get_current_packages())
        print('')


    #This method is called by the deliver method.
    #It takes the distance between the previous package and the current package and adds that to the truck time.
    # The actual time assumes a speed of 18 mph.
    #O(1)



    def increment_truck_time(self, distance, truck):
        speed = 18
        truck.distance += distance
        travel_time = timedelta(hours=distance/speed)
        truck.time += travel_time


    # This method never got used.
    # It would have been for getting the time but not actually incrementing the truck time.

    #O(1)
    def get_time(self, distance, truck):
        speed = 18
        travel_time = timedelta(hours=distance/speed)
        travel_time += truck.time

        return travel_time

    #This method is used to find out the last delivered package.
    #It loops through the packages in the truck until package.delivered == True.

    #O(n)

    # This method is used for looking up various stats about the packages.
    # Its a little messy but it works.

    #O(n)
    def lookupStats(self):
        print("What would you like to lookup by?")
        print("1. Package ID")
        print("2. Delivery Address")
        print("3. Delivery Deadline")
        print("4. Delivery City")
        print("5. Delivery Zip Code")
        print("6. Package Weight")
        print("7. Delivery Status")
        print("8. Back to Simulation")
        i = input()
        if i == "1":
            search_results = []
            print("Enter Package ID")
            i = input()
            found = False
            for package in self.all_packages:
                if package.package_id == i:
                    search_results.append(package)
                    print("Package found")
                    # print package info here
                    found = True
            if not found and len(search_results) == 0:
                print("Package not found")
                self.lookupStats()
            elif len(search_results) > 0:
                print("Search results:")
                j = 0
                for package in search_results:
                    print(str(j) + " : Package with ID " + package.package_id)
                    j += 1
                print("Enter the number of the package you would like to view")
                i = input()
                print(search_results[int(i)])
                input("Press enter to continue")
                self.lookupStats()
        elif i == "2":
            search_results = []
            print("Enter Delivery Address")
            i = input()
            for package in self.all_packages:
                if package.address == i:
                    search_results.append(package)
                    print("Package found")
                    # print package info here
                    found = True
            if not found and len(search_results) == 0:
                print("Package not found")
                self.lookupStats()
            elif len(search_results) > 0:
                print("Search results:")
                j = 0
                for package in search_results:
                    print(str(j) + " : Package with ID " + package.package_id)
                    j += 1
                print("Enter the number of the package you would like to view")
                i = input()
                print(search_results[int(i)])
                input("Press enter to continue")
                self.lookupStats()
        elif i == "3":
            search_results = []
            print("Enter Delivery Deadline")
            print("HH:MM")
            i = input()
            for package in self.all_packages:
                if package.deadline == i:
                    search_results.append(package)
                    print("Package found")
                    # print package info here
                    found = True
            if not found and len(search_results) == 0:
                print("Package not found")
                self.lookupStats()
            elif len(search_results) > 0:
                print("Search results:")
                j = 0
                for package in search_results:
                    print(str(j) + " : Package with ID " + package.package_id)
                    j += 1
                print("Enter the number of the package you would like to view")
                i = input()
                print(search_results[int(i)])
                input("Press enter to continue")
                self.lookupStats()
        elif i == "4":
            search_results = []
            print("Enter Delivery City")
            i = input()
            for package in self.all_packages:
                if package.city == i:
                    search_results.append(package)
                    print("Package found")
                    # print package info here
                    found = True
            if not found and len(search_results) == 0:
                print("Package not found")
                self.lookupStats()
            elif len(search_results) > 0:
                print("Search results:")
                j = 0
                for package in search_results:
                    print(str(j) + " : Package with ID " + package.package_id)
                    j += 1
                print("Enter the number of the package you would like to view")
                i = input()
                print(search_results[int(i)])
                input("Press enter to continue")
                self.lookupStats()
        elif i == "5":
            search_results = []
            print("Enter Delivery Zip Code")
            i = input()
            for package in self.all_packages:
                if package.zip_code == i:
                    search_results.append(package)
                    print("Package found")
                    # print package info here
                    found = True
            if not found and len(search_results) == 0:
                print("Package not found")
                self.lookupStats()
            elif len(search_results) > 0:
                print("Search results:")
                j = 0
                for package in search_results:
                    print(str(j) + " : Package with ID " + package.package_id)
                    j += 1
                print("Enter the number of the package you would like to view")
                i = input()
                print(search_results[int(i)])
                input("Press enter to continue")
                self.lookupStats()
        elif i == "6":
            search_results = []
            print("Enter Package Weight")
            i = input()
            search_results = []
            found = False
            for package in self.all_packages:
                if package.weight == i:
                    search_results.append(package)
                    print("Package found")
                    # print package info here
                    found = True
            if not found and len(search_results) == 0:
                print("Package not found")
                self.lookupStats()
            elif len(search_results) > 0:
                print("Search results:")
                j = 0
                for package in search_results:
                    print(str(j) + " : Package with ID " + package.package_id)
                    j += 1
                print("Enter the number of the package you would like to view")
                i = input()
                print(search_results[int(i)])
                input("Press enter to continue")
                self.lookupStats()
        elif i == "7":
            search_results = []
            print("Enter Delivery Status")
            i = input()
            for package in self.all_packages:
                if package.delivery_status == i:
                    search_results.append(package)
                    print("Package found")
                    # print package info here
                    found = True
            if not found and len(search_results) == 0:
                print("Package not found")
                self.lookupStats()
            elif len(search_results) > 0:
                print("Search results:")
                j = 0
                for package in search_results:
                    print(str(j) + " : Package with ID " + package.package_id)
                    j += 1
                print("Enter the number of the package you would like to view")
                i = input()
                print(search_results[int(i)])
                input("Press enter to continue")
                self.lookupStats()
        elif i == "8":
            return
        else:
            print("Invalid input")
            input("Press enter to continue")
            self.lookupStats()






