# Class Runway to store info about runways

from validation import validate_runway
from constraint_checking import check_runway_constraints   


class Runway:

    def __init__(self, length, availability, assigned_flight,
                 runway_id, usage, maintenance_window,
                 maintenance_from, maintenance_to):

        self.length = int(length)
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


def auto_allocate_runways():

    from data_loader import load_flights
    from allocation_engine import allocate_flight

    flights = load_flights()

    for flight in flights:

        # skip already allocated
        if flight.aircraft == "NA":
            continue

        # try allocate runway through full system
        allocate_flight(flight)

# Write runway data into file
def writeData():

    print("Runway Module")
    n = int(input("Enter number of runways: "))
    existing = load_runways()

    new_runway_added = False

    with open("runwaydetails.txt", "a") as file:

        for _ in range(n):

            runway_id = input("Runway ID: ")
            length = input("Length: ")
            availability = input("Availability (Free/Occupied): ")
            assigned_flight = "NA"
            usage = input("Usage (Takeoff/Landing/Both): ")
            maintenance_window = input("Maintenance (Yes/No): ")
            maintenance_from = input("From (NA if none): ")
            maintenance_to = input("To (NA if none): ")

            # 🔹 validation
            if not validate_runway(length, availability, usage, maintenance_window):
                continue

            # duplicate check
            if any(r.runway_id == runway_id for r in existing):
                print("Duplicate runway")
                continue

            # maintenance check
            if maintenance_window == "No" and (maintenance_from != "NA" or maintenance_to != "NA"):
                print("Invalid maintenance data")
                continue

            if maintenance_window == "Yes" and (maintenance_from == "NA" or maintenance_to == "NA"):
                print("Missing maintenance time")
                continue

            file.write(",".join([
                length, availability, assigned_flight,
                runway_id, usage, maintenance_window,
                maintenance_from, maintenance_to
            ]) + "\n")

            existing.append(Runway(
                length, availability, assigned_flight,
                runway_id, usage, maintenance_window,
                maintenance_from, maintenance_to
            ))

            new_runway_added = True

    print(" Runways added")

    if new_runway_added:
        auto_allocate_runways()