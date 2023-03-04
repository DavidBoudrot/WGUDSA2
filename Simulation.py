
import time as t

import threading
from datetime import timedelta, datetime, time
class Simulation:
    all_packages = []
    totalmiles = 0
    packsdelivered = 0
    trucks = []
    time = "8:00"
    # Mutex that will be used to keep track of the time
    # Only one thread can access this at a time
    # The thread will say; Hey I'm going to access the time now
    # If a different thread is already accessing the time, it will wait until the other thread is done
    # If a thread is accessing the time and it wants to deliver a package that has a delivery time after
    # the current time, it will pass and give time access to another thread.
    def __init__(self, trucks, all_packages):
        self.trucks = trucks
        self.totalmiles = 0
        self.all_packages = all_packages

    #This is where the simulation will run
    def run_simulation(self):
        # Create a lock for synchronizing thread access
        lock = threading.Lock()
        self.time = datetime.strptime("8:00", '%H:%M')
        packages = self.trucks[0].get_current_packages().get_path()
        print(len(packages))
        packages = self.trucks[1].get_current_packages().get_path()
        print(len(packages))
        packages = self.trucks[2].get_current_packages().get_path()
        print(len(packages))
        # Wait for user input to start the simulation
        input("Press Enter to start the simulation")
        # Start the delivery threads for trucks 1 and 2
        self.thread1 = threading.Thread(target=self.deliver_packages, args=(self.trucks[0], "1", lock))
        self.thread2 = threading.Thread(target=self.deliver_packages, args=(self.trucks[1], "2", lock))



        self.thread1.start()
        self.thread2.start()


        self.thread1.join()
        self.thread2.join()

        #get the time for truck 3
        # self.time = self.trucks[0].time
        # self.trucks[2].time = self.time
        #
        # self.thread3.start()
        # self.thread1.join()
        # self.thread3.join()
        # self.thread2.join()


    def deliver_packages(self, truck, truckID, lock):
        print(f"Starting thread {truckID}")
    #Here we need to check if the truck is ready ready to deliver.
        #If the departing time is greater than the current time, we need to wait
        # while truck.time > self.time:
        #     print(f"Thread {truckID} is waiting for the time to catch up")
        #     print("Current time: " + self.time.strftime("%I:%M %p"))
        #     print("Truck time: " + truck.time.strftime("%I:%M %p"))
        #     continue
        #Okay now we know the truck is ready to deliver
        #We just need to deliver the packages by order of clock time.
        #This is where we will need to use the mutex to keep track of the time
        #Getting the packages from the truck
        packages = truck.get_current_packages().get_path()
        # Setting the packages status to en route
        for package in packages:
            package.setDeliveryStatus("En Route")
        # Delivering the packages
        for i, package in enumerate(packages):
            print("getting packages in thread " + truckID)
            with lock:
                #This is where We need to find the lower time of the two trucks
                #If the package time is greater than the current time, we need to wait
                #We just need to make sure that self.time stays up to date
                while truck.time > self.time:
                    print(f"Thread {truckID} is waiting for the time to catch up")
                    print("Current time: " + self.time.strftime("%I:%M %p"))
                    print("Package delivery time: " + truck.time.strftime("%I:%M %p"))
                        #This is basically saying that truck 1 is done and we have to start another thread or else the program will hang

                    continue

                if package.special_notes == "Hub":
                    print("Reloading packages, going back to hub")
                else:

                    self.print_package_info(package, truck)
                    package.delivery_status = "Delivered"
                    package.timestamp = truck.time
                    self.packsdelivered += 1

                # Check if next package is ready to be delivered
                if i + 1 < len(packages):
                    # If there is another package to deliver increment the time
                    next_package = packages[i + 1]
                    truck = self.increment_time(package, next_package, truck)
                else:
                    # No more packages to deliver
                    print(f"That's it for truck {truckID}\nPackages delivered: {str(self.packsdelivered)}")
                    self.time = truck.time
                    print(truck.truck_id)
                    print("Current time: " + self.time.strftime("%I:%M %p"))
                    print("Truck time: " + truck.time.strftime("%I:%M %p"))
                    return
    def print_package_info(self, package, truck):
        delivery_time_str = truck.time.strftime("%I:%M %p")
        print(f"Package {package.package_id} Delivered at {delivery_time_str} on truck {truck.truck_id} to {package.address}")
        print(f"Package ID: {package.package_id}")
        if package.special_notes:
            print(f"Special Notes: {package.special_notes}")
        # if package.deadline != "EOD":
        #     print(f"Deadline: {package.deadline}")
        #     print(f"Package was delivered at {delivery_time_str} on {truck.time.strftime('%m/%d/%Y')}")
        #
        #     if self.parseTimeFromString(package.deadline) < package.timestamp:
        #         print("Package was late")

    def reload_truck(self, truck):
        print("Reloading truck 1")
        self.trucks[0].time = truck.time
        self.time = truck.time
        self.trucks[0].current_packages = self.trucks[3].get_current_packages()
        self.reloaded = True

    def increment_time(self, prev, current, truck):
        speed = 18  # miles per hour
        distance = prev.get_distance(current)
        travel_time = timedelta(hours=distance/speed)
        truck.time += travel_time
        print("Previous time " + self.time.strftime("%I:%M %p"))
        self.time = truck.time
        print("Updated time: " + self.time.strftime("%I:%M %p"))
        return truck

    def parseTimeFromString(self, time_str):
        datetime_obj = datetime.strptime(time_str, '%I:%M %p')
        return datetime_obj.strftime('%H:%M')

    def parseTime(self, time_str):
        datetime_obj = datetime.strptime(time_str, '%I:%M %p')
        return datetime_obj



# This is kinda messy I'm sorry for anyone reading this. I just hacked it together.
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


















