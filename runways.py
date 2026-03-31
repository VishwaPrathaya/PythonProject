# Class Runway to store info about runways

from validation import validate_runway
from constraint_checking import check_runway_constraints   # ✅ ADDED


class Runway:

    def __init__(self, length, availability, assigned_flight,
                 runway_id, usage, maintenance_window,
                 maintenance_from, maintenance_to):

        self.length = length
        self.availability = availability
        self.assigned_flight = assigned_flight
        self.runway_id = runway_id
        self.usage = usage
        self.maintenance_window = maintenance_window
        self.maintenance_from = maintenance_from
        self.maintenance_to = maintenance_to

    # Display runway details
    def display(self):
        print("Runway ID:", self.runway_id,
              "| Length:", self.length,
              "| Status:", self.availability,
              "| Assigned Flight:", self.assigned_flight,
              "| Usage:", self.usage,
              "| Maintenance:", self.maintenance_window,
              "| From:", self.maintenance_from,
              "| To:", self.maintenance_to)


# Load runway data from file
def load_runways():

    runways = []

    try:
        with open("runwaydetails.txt", "r") as f:

            for line in f:
                data = line.strip().split(",")

                if len(data) != 8:
                    print("Invalid runway data:", line)
                    continue

                runway = Runway(*data)
                runways.append(runway)

    except FileNotFoundError:
        print("runwaydetails.txt not found. File will be created when data is added.")

    return runways


# Display runway details
def display_runways():

    runways = load_runways()

    if len(runways) == 0:
        print("\nNo runway data available.")
        return

    print("\n--- Runway Details ---")

    for r in runways:
        r.display()


# Write runway data into file
def writeData():

    print("Airport Operations Management System - Runway Module")

    n = int(input("Enter number of runways to add: "))

    with open("runwaydetails.txt", "a") as file:

        for i in range(n):

            print("\nEnter details for Runway", i + 1)

            runway_id = input("Runway ID: ")
            length = input("Runway Length (meters): ")
            availability = input("Availability Status (Free/Occupied): ")
            assigned_flight = input("Assigned Flight Number (NA if none): ")
            usage = input("Usage Restriction (Takeoff/Landing/Both): ")
            maintenance_window = input("Maintenance Window Available (Yes/No): ")
            maintenance_from = input("Maintenance From (time or NA): ")
            maintenance_to = input("Maintenance To (time or NA): ")

            # ✅ STEP 1: VALIDATION
            if not validate_runway(length, availability, usage, maintenance_window):
                print("Invalid input. Skipping this entry...\n")
                continue

            # ✅ STEP 2: CONSTRAINT CHECK
            if not check_runway_constraints(load_runways(), runway_id):
                print("Constraint violation. Skipping this entry...\n")
                continue

            # Only valid + constraint-safe data stored
            r = Runway(length, availability, assigned_flight,
                       runway_id, usage, maintenance_window,
                       maintenance_from, maintenance_to)

            file.write(length + "," +
                       availability + "," +
                       assigned_flight + "," +
                       runway_id + "," +
                       usage + "," +
                       maintenance_window + "," +
                       maintenance_from + "," +
                       maintenance_to + "\n")

    print("\nRunways added successfully!")
    display_runways()