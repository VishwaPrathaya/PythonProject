from flights import load_flights
from passenger import load_passengers, seats_used
from validation import validate_passenger_booking, validate_time_range
from passenger_allocation import allocate_passengers
from passenger_search import search_flights


def offer_rebooking_for_cancelled_flight(fno):
    """Offer rebooking to passengers booked on cancelled flight `fno`.

    Interactive: asks each passenger whether they want to be rebooked to a suitable alternative.
    """
    flights = load_flights()
    passengers = load_passengers()

    original = next((f for f in flights if f.fno == fno), None)
    if not original:
        print(f"Original flight {fno} not found for rebooking")
        return

    affected = [p for p in passengers if p.fno == fno]
    if not affected:
        print(f"No passengers booked on flight {fno}")
        return

    # candidate flights: same origin/destination and not the cancelled one
    candidates = [fl for fl in flights if fl.fno != fno and fl.origin == original.origin and fl.destination == original.destination]

    for p in affected:
        print(f"\nPassenger {p.pid} | {p.name} | Seat {p.seat}")
        choice = input("Offer rebooking to other flights? (yes/no): ")
        if choice.lower() != "yes":
            continue

        available = []
        for fl in candidates:
            used = seats_used(fl.fno)
            if used < fl.capacity:
                available.append(fl)

        if not available:
            print(" No alternative flights with available seats found.")
            continue

        print("Available alternatives:")
        for fl in available:
            print(f"{fl.fno} | {fl.origin} -> {fl.destination} | Dep: {fl.dep} | Seats used: {seats_used(fl.fno)}/{fl.capacity}")

        newf = input("Choose Flight ID to rebook (or blank to skip): ")
        if not newf:
            continue

        target = next((fl for fl in available if fl.fno == newf), None)
        if not target:
            print("Invalid flight chosen. Skipping passenger.")
            continue

        # assign a new seat id (simple incremental rebook seat)
        new_seat = f"RB{seats_used(target.fno) + 1}"

        # update passenger in memory
        p.fno = target.fno
        p.seat = new_seat

        print(f" Passenger {p.pid} rebooked to {target.fno} seat {new_seat}")

    # persist passenger file
    with open("passenger.csv", "w") as pf:
        for p in passengers:
            pf.write(",".join([
                p.pid, p.name, p.fno,
                p.seat, p.ticket_class, p.status,
                p.counter_id
            ]) + "\n")

    # trigger re-allocation to assign counters for any newly rebooked passengers
    allocate_passengers()


def offer_rebooking_notifications(fno):
    """Create operator notifications for passengers on cancelled flight `fno`.

    Writes `rebooking_notifications.csv` entries with suggested alternative flight IDs
    so an operator can review and approve rebookings.
    """
    flights = load_flights()
    passengers = load_passengers()

    original = next((f for f in flights if f.fno == fno), None)
    if not original:
        print(f"Original flight {fno} not found for rebooking notifications")
        return

    affected = [p for p in passengers if p.fno == fno]
    if not affected:
        print(f"No passengers booked on flight {fno}")
        return

    # candidate flights: same origin/destination and not the cancelled one
    candidates = [fl for fl in flights if fl.fno != fno and fl.origin == original.origin and fl.destination == original.destination]

    notif_lines = []
    for p in affected:
        suggestions = []
        for fl in candidates:
            used = seats_used(fl.fno)
            if used < fl.capacity:
                suggestions.append(fl.fno)

        line = ",".join([
            p.pid, p.name, p.fno, "|".join(suggestions) if suggestions else "",
            "Pending"
        ])
        notif_lines.append(line)

    # append notifications file
    with open("rebooking_notifications.csv", "a") as nf:
        for l in notif_lines:
            nf.write(l + "\n")

    print(f"Wrote {len(notif_lines)} rebooking notifications to rebooking_notifications.csv")


# ---------------- VIEW SCHEDULED FLIGHTS (TIME RANGE) ----------------
def view_scheduled_flights():

    flights = load_flights()

    print("\n=== VIEW SCHEDULED FLIGHTS ===")
    start = input("From time: ")
    end = input("To time: ")

    if not validate_time_range(start, end):
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

        if not validate_time_range(start, end):
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
        f.write(f"{pid},{name},{selected.fno},{seat},{ticket_class},Booked,NA\n")

    print(f"- Booking successful — {ticket_class} class")
    print(f"   Flight : {selected.fno} | {selected.origin} → {selected.destination}")
    print(f"   Seat   : {seat}")

    # ---------------- AUTO ALLOCATION TRIGGER ----------------
    # assign counter from existing allocation if present
    from allocation_engine import load_allocations
    allocs = load_allocations()
    alloc = allocs.get(selected.fno)
    assigned_counter = "NA"
    if alloc and len(alloc) > 6:
        # allocation stores counters as pipe-separated ids
        assigned_counter = alloc[6].split("|")[0]

    if assigned_counter != "NA":
        # update the newly added passenger record with counter assignment
        from passenger import load_passengers
        passengers = load_passengers()
        for p in passengers:
            if p.pid == pid and p.fno == selected.fno:
                p.counter_id = assigned_counter
        with open("passenger.csv", "w") as pf:
            for p in passengers:
                pf.write(",".join([
                    p.pid, p.name, p.fno,
                    p.seat, p.ticket_class,
                    p.status, p.counter_id
                ]) + "\n")

        print(f"- Assigned counter {assigned_counter} to passenger {pid}")

    allocate_passengers()