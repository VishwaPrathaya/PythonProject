from flights import load_flights
from passenger import load_passengers, seats_used
from validation import validate_passenger_booking
from passenger_allocation import allocate_passengers
from passenger_search import search_flights


# ---------------- VIEW SCHEDULED FLIGHTS (TIME RANGE) ----------------
def view_scheduled_flights():

    flights = load_flights()

    print("\n=== VIEW SCHEDULED FLIGHTS ===")
    start = input("From time: ")
    end = input("To time: ")

    if not start.isdigit() or not end.isdigit():
        print("- Invalid time range")
        return

    matches = search_flights(flights, time_from=int(start), time_to=int(end))

    if not matches:
        print("No flights scheduled in this time range")
        return

    print(f"\n--- Flights from {start} to {end} ---")
    for f in matches:
        print(f"{f.fno} | {f.origin} → {f.destination} | Arr: {f.arr} | Dep: {f.dep} | {f.flight_type}")


# ---------------- BOOK FLIGHT ----------------
def book_flight():

    flights = load_flights()
    passengers = load_passengers()

    print("\n=== BOOK FLIGHT ===")
    print("1. By Flight ID")
    print("2. By Origin, Destination and Time Range")

    choice = input("Select option: ")

    selected = None

    # ---------------- OPTION 1: BY FLIGHT ID ----------------
    if choice == "1":

        fno = input("Enter Flight ID: ")
        selected = next((f for f in flights if f.fno == fno), None)

        if not selected:
            print("- Flight not found")
            return

        print(f"\n{selected.fno} | {selected.origin} → {selected.destination} | Arr: {selected.arr} | Dep: {selected.dep} | {selected.flight_type}")

    # ---------------- OPTION 2: BY ROUTE + TIME RANGE ----------------
    elif choice == "2":

        origin = input("Origin: ")
        destination = input("Destination: ")
        start = input("From time: ")
        end = input("To time: ")

        if not start.isdigit() or not end.isdigit():
            print("- Invalid time range")
            return

        matches = search_flights(
            flights,
            origin=origin,
            destination=destination,
            time_from=int(start),
            time_to=int(end)
        )

        if not matches:
            print("No flights found for this route and time range")
            return

        print("\nAvailable flights:")
        for f in matches:
            print(f"{f.fno} | {f.origin} → {f.destination} | Arr: {f.arr} | Dep: {f.dep} | {f.flight_type}")

        fno = input("\nChoose Flight ID: ")
        selected = next((f for f in matches if f.fno == fno), None)

        if not selected:
            print("- Flight not found")
            return

    else:
        print(" Invalid choice")
        return

    # ---------------- PASSENGER INPUT ----------------
    pid = input("Passenger ID: ")
    name = input("Name: ")
    seat = input("Seat No: ")

    print("\nTicket Class:")
    print("1. Economy")
    print("2. Business")
    print("3. First")
    cls_choice = input("Choose: ")

    if cls_choice == "1":
        ticket_class = "Economy"
    elif cls_choice == "2":
        ticket_class = "Business"
    elif cls_choice == "3":
        ticket_class = "First"
    else:
        print("Invalid choice, defaulting to Economy")
        ticket_class = "Economy"

    # ---------------- VALIDATION ----------------
    if not validate_passenger_booking(pid, name, selected, seat, passengers, seats_used):
        return

    # ---------------- SAVE BOOKING ----------------
    with open("passenger.csv", "a") as f:
        f.write(f"{pid},{name},{selected.fno},{seat},{ticket_class},Booked\n")

    print(f"- Booking successful — {ticket_class} class")
    print(f"   Flight : {selected.fno} | {selected.origin} → {selected.destination}")
    print(f"   Seat   : {seat}")

    # ---------------- AUTO ALLOCATION TRIGGER ----------------
    allocate_passengers()