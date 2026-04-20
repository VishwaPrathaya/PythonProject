from validation import validate_flight
from constraint_checking import validate_flight_constraints
from data_loader import load_flights
from allocation_engine import allocate_flight
from models import Flight




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

    with open("flights.txt", "a") as file:

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

            # 🔹 STEP 1: VALIDATION
            if not validate_flight(fno, arr, dep, flight_type, date, existing):
                print("❌ Validation failed\n")
                continue

            # 🔹 STEP 2: CONSTRAINT CHECK
            if not validate_flight_constraints(existing, fno, int(arr), int(dep)):
                print("❌ Constraint violation\n")
                continue

            # 🔹 CREATE OBJECT (NO AIRCRAFT YET)
            new_flight = Flight(
                fno, airline, origin, destination,
                arr, dep, date, "NA", flight_type
            )

            # 🔹 SAVE BASIC FLIGHT FIRST
            file.write(",".join([
                fno, airline, origin, destination,
                arr, dep, date, "NA", flight_type, capacity
            ]) + "\n")

            existing.append(new_flight)

            print("✅ Flight added successfully")

            # 🔥🔥🔥 IMPORTANT (YOU MISSED THIS BEFORE)
            # AUTO ALLOCATION TRIGGER
            allocate_flight(new_flight)

    display_flights()