from validation import validate_flight, validate_numeric, validate_flight_type
from constraint_checking import validate_flight_constraints
from allocation_engine import allocate_flight



class Flight:

    def __init__(self, fno, airline, origin, destination,
                 arr, dep, date, aircraft="NA",
                 flight_type="Domestic", capacity="100"):

        self.fno = fno
        self.airline = airline
        self.origin = origin
        self.destination = destination
        self.arr = arr
        self.dep = dep
        self.date = date
        self.aircraft = aircraft
        self.flight_type = flight_type
        self.capacity = int(capacity)


# ------------ LOAD FLIGHT ---------------
def load_flights():

    flights = []

    try:
        with open("flights.csv", "r") as f:
            for line in f:
                data = line.strip().split(",")

                if len(data) != 10:
                    continue

                flights.append(Flight(*data))

    except FileNotFoundError:
        pass

    return flights



# ---------------- DISPLAY ----------------
def display_flights():

    flights = load_flights()

    if not flights:
        print("\nNo flight records found.")
        return

    print("\n--- Flight Details ---")

    for f in flights:
        print(f"Flight: {f.fno} | Airline: {f.airline} | {f.origin}->{f.destination} | "
              f"Arr: {f.arr} | Dep: {f.dep} | Date: {f.date} | Aircraft: {f.aircraft}")


# ---------------- WRITE DATA ----------------
def writeData():

    print("\n===== Flight Management Module =====")

    n = int(input("Enter number of flights: "))

    existing = load_flights()

    with open("flights.csv", "a") as file:

        for i in range(n):

            print(f"\nEnter Flight {i + 1} Details")

            fno = input("Flight Number: ")
            airline = input("Airline: ")
            origin = input("Origin: ")
            destination = input("Destination: ")
            arr = input("Arrival Time: ")
            dep = input("Departure Time: ")
            date = input("Date (DD-MM-YYYY): ")
            flight_type = input("Flight Type (Domestic/International): ")
            capacity = input("Capacity: ")

            # - STEP 1: VALIDATION
            if not validate_flight(fno, arr, dep, flight_type, date, existing):
                print(" Validation failed\n")
                continue

            # - STEP 2: CONSTRAINT CHECK
            if not validate_flight_constraints(existing, fno, int(arr), int(dep)):
                print("- Constraint violation\n")
                continue

            # - CREATE OBJECT 
            new_flight = Flight(
                fno, airline, origin, destination,
                arr, dep, date, "NA", flight_type, capacity
            )

            # - SAVE BASIC FLIGHT FIRST
            file.write(",".join([
                fno, airline, origin, destination,
                arr, dep, date, "NA", flight_type, capacity
            ]) + "\n")

            existing.append(new_flight)

            print(" Flight added successfully")

            # AUTO ALLOCATION TRIGGER
            from allocation_engine import refresh_flight_allocation
            refresh_flight_allocation(new_flight.fno)

    display_flights()

def remove_flight():

    fno = input("Enter Flight Number to remove: ")

    flights = load_flights()
    updated = []

    target = None

    for f in flights:
        if f.fno == fno:
            target = f
        else:
            updated.append(f)

    if not target:
        print("- Flight not found")
        return

    # - rewrite flights file
    with open("flights.csv", "w") as file:
        for f in updated:
            file.write(",".join([
                f.fno, f.airline, f.origin, f.destination,
                f.arr, f.dep, f.date, f.aircraft,
                f.flight_type, str(f.capacity)
            ]) + "\n")

    print(f"- Flight {fno} removed from system")

    # - remove allocation + free resources
    from allocation_engine import remove_allocation_for_flight, system_rebalance
    remove_allocation_for_flight(fno, auto_reallocate=False)

    # - perform centralized rebalance after freeing resources
    print(" Attempting system rebalance for pending flights...")
    system_rebalance()


def update_flight():

    flights = load_flights()

    if not flights:
        print("No flights available")
        return

    fno = input("Enter Flight Number to update: ")

    target = next((f for f in flights if f.fno == fno), None)

    if not target:
        print("Flight not found")
        return

    print(f"\nCurrent: {target.fno} | {target.airline} | {target.origin}->{target.destination} | "
          f"{target.arr}-{target.dep} | {target.date} | {target.flight_type} | Aircraft: {target.aircraft}")

    print("\nLeave blank to keep existing value\n")

    airline = input(f"Airline [{target.airline}]: ").strip()
    origin = input(f"Origin [{target.origin}]: ").strip()
    destination = input(f"Destination [{target.destination}]: ").strip()
    arr = input(f"Arrival [{target.arr}]: ").strip()
    dep = input(f"Departure [{target.dep}]: ").strip()
    date = input(f"Date [{target.date}]: ").strip()
    flight_type = input(f"Type [{target.flight_type}]: ").strip()
    capacity = input(f"Capacity [{target.capacity}]: ").strip()

    # APPLY CHANGES
    if airline:
        target.airline = airline

    if origin:
        target.origin = origin

    if destination:
        target.destination = destination

    if arr:
        if not validate_numeric(arr, "Invalid arrival time"):
            return
        target.arr = arr

    if dep:
        if not validate_numeric(dep, "Invalid departure time"):
            return
        target.dep = dep

    if date:
        target.date = date

    if flight_type:
        if not validate_flight_type(flight_type):
            return
        target.flight_type = flight_type

    if capacity:
        if not validate_numeric(capacity, "Invalid capacity"):
            return
        target.capacity = int(capacity)

    #  If timing changed → remove old allocation
    from allocation_engine import remove_allocation_for_flight, system_rebalance

    print(" Removing old allocation (if any)...")
    remove_allocation_for_flight(fno, auto_reallocate=False)

    # SAVE UPDATED FILE
    with open("flights.csv", "w") as f:
        for fl in flights:
            f.write(",".join([
                fl.fno, fl.airline, fl.origin, fl.destination,
                fl.arr, fl.dep, fl.date, fl.aircraft,
                fl.flight_type, str(fl.capacity)
            ]) + "\n")

    print(" Flight updated successfully")

    # - CENTRALIZED SYSTEM REBALANCE
    print("- Attempting centralized system rebalance...")
    system_rebalance()