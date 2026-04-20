from data_loader import load_flights
from passenger import load_passengers
from validation import validate_passenger_booking
from passenger_allocation import allocate_passengers
from passenger_search import search_flights   # assuming you have this
from passenger import seats_used   # add seats_used here


# ---------------- BOOK FLIGHT ----------------
def book_flight():

    flights = load_flights()
    passengers = load_passengers()

    print("\n=== BOOK FLIGHT ===")
    print("1. By Flight ID")
    print("2. By Route (Origin-Destination)")
    print("3. By Time")

    choice = input("Select option: ")

    selected = None

    # ---------------- OPTION 1 ----------------
    if choice == "1":

        fno = input("Enter Flight ID: ")
        selected = next((f for f in flights if f.fno == fno), None)

    # ---------------- OPTION 2 ----------------
    elif choice == "2":

        origin = input("Origin: ")
        destination = input("Destination: ")

        matches = search_flights(flights, origin=origin, destination=destination)

        if not matches:
            print("No flights found for route")
            return

        for f in matches:
            print(f"{f.fno} | {f.origin} → {f.destination} | {f.arr}-{f.dep}")

        fno = input("Choose Flight ID: ")
        selected = next((f for f in matches if f.fno == fno), None)

    # ---------------- OPTION 3 ----------------
    elif choice == "3":

        time = input("Enter Time: ")

        matches = search_flights(flights, time=time)

        if not matches:
            print("No flights found for time")
            return

        for f in matches:
            print(f"{f.fno} | {f.origin} → {f.destination} | {f.arr}-{f.dep}")

        fno = input("Choose Flight ID: ")
        selected = next((f for f in matches if f.fno == fno), None)

    else:
        print("❌ Invalid choice")
        return

    # ---------------- FLIGHT VALIDATION ----------------
    if not selected:
        print("❌ Flight not found")
        return

    # ---------------- PASSENGER INPUT ----------------
    pid = input("Passenger ID: ")
    name = input("Name: ")
    seat = input("Seat No: ")

    # ---------------- VALIDATION CALL ----------------
    if not validate_passenger_booking(
    pid,
    name,
    selected,
    seat,
    passengers,
    seats_used   # ← fixed
    ):
        return

    # ---------------- SAVE BOOKING ----------------
    with open("passenger.txt", "a") as f:
        f.write(f"{pid},{name},{selected.fno},{seat},Economy,Booked\n")

    print("✅ Booking successful")

    # ---------------- AUTO ALLOCATION TRIGGER ----------------
    allocate_passengers()