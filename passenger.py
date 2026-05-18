from validation import validate_passenger_status
class Passenger:

    def __init__(self, pid, name, fno, seat, ticket_class="Economy", status="Booked", counter_id="NA"):
        self.pid = pid
        self.name = name
        self.fno = fno
        self.seat = seat
        self.ticket_class = ticket_class
        self.status = status
        self.counter_id = counter_id


# ---------------- LOAD ----------------
def load_passengers():

    lst = []

    try:
        with open("passenger.csv") as f:
            for line in f:
                data = line.strip().split(",")

                if len(data) == 4:
                    pid, name, fno, seat = data
                    lst.append(Passenger(pid, name, fno, seat))
                elif len(data) == 6:
                    pid, name, fno, seat, ticket_class, status = data
                    lst.append(Passenger(pid, name, fno, seat, ticket_class, status))
                elif len(data) == 7:
                    pid, name, fno, seat, ticket_class, status, counter_id = data
                    lst.append(Passenger(pid, name, fno, seat, ticket_class, status, counter_id))
    except FileNotFoundError:
        pass

    return lst


# ---------------- DISPLAY ----------------
def display_passengers():

    passengers = load_passengers()

    if not passengers:
        print("No passengers found")
        return

    print("\n--- PASSENGERS ---")
    for p in passengers:
        counter_display = p.counter_id if p.counter_id != "NA" else "Unassigned"
        print(f"{p.pid} | {p.name} | {p.fno} | {p.seat} | {p.ticket_class} | {p.status} | {counter_display}")


# ---------------- SEAT COUNT ----------------
def seats_used(fno):
    return sum(1 for p in load_passengers() if p.fno == fno)


# ---------------- WRITE ----------------
def writeData():

    from flights import load_flights
    from validation import validate_passenger_booking, validate_ticket_class, validate_passenger_status
    from passenger_allocation import allocate_passengers

    n = int(input("Passenger count: "))
    existing = load_passengers()
    flights = load_flights()

    new_added = False
    changed_flights = set()

    with open("passenger.csv", "a") as f:

        for _ in range(n):

            pid = input("Passenger ID: ")
            name = input("Name: ")
            fno = input("Flight No: ")
            seat = input("Seat No: ")
            ticket_class = input("Class (Economy/Business/First): ")
            status = input("Status (Booked/Checked-In/Boarded): ")

            if not validate_ticket_class(ticket_class):
                continue

            if not validate_passenger_status(status):
                continue

            selected = next((fl for fl in flights if fl.fno == fno), None)

            if not validate_passenger_booking(pid, name, selected, seat, existing, seats_used):
                continue

            f.write(",".join([pid, name, fno, seat, ticket_class, status, "NA"]) + "\n")

            existing.append(Passenger(pid, name, fno, seat, ticket_class, status, "NA"))
            changed_flights.add(fno)
            new_added = True

            print("- Passenger added")

    if new_added:
        print("- Passenger data updated → re-evaluating allocations")

        from allocation_engine import refresh_flight_allocation

        for fno in sorted(changed_flights):
            refresh_flight_allocation(fno)

        allocate_passengers()


# ---------------- REMOVE ----------------
def remove_passenger():

    pid = input("Enter Passenger ID to remove: ")

    passengers = load_passengers()
    updated = []

    found = False

    for p in passengers:
        if p.pid == pid:
            found = True
            print(f" Removing passenger {p.name} from Flight {p.fno}")
            continue
        updated.append(p)

    if not found:
        print("- Passenger not found")
        return

    # - SAVE FILE
    with open("passenger.csv", "w") as f:
        for p in updated:
            f.write(",".join([
                p.pid, p.name, p.fno,
                p.seat, p.ticket_class, p.status,
                p.counter_id
            ]) + "\n")

    print("- Passenger removed successfully")

    # - TRIGGER
    print("- Updating flight passenger status...")
    from passenger_allocation import allocate_passengers
    allocate_passengers()


# ---------------- UPDATE ----------------
def update_passenger():

    passengers = load_passengers()

    if not passengers:
        print("No passengers available")
        return

    pid = input("Enter Passenger ID to update: ")

    target = next((p for p in passengers if p.pid == pid), None)

    if not target:
        print("Passenger not found")
        return

    print(f"\nCurrent: {target.pid} | {target.name} | {target.fno} | {target.seat} | {target.status}")
    print("Leave blank to keep current value\n")

    name = input(f"Name [{target.name}]: ").strip()
    seat = input(f"Seat [{target.seat}]: ").strip()
    status = input(f"Status [{target.status}]: ").strip()

    # - APPLY CHANGES
    if name:
        target.name = name

    if seat:
        target.seat = seat

    if status:
        if not validate_passenger_status(status):
            return
        target.status = status

    # - SAVE FILE
    with open("passenger.csv", "w") as f:
        for p in passengers:
            f.write(",".join([
                p.pid, p.name, p.fno,
                p.seat, p.ticket_class, p.status,
                p.counter_id
            ]) + "\n")

    print(f"- Passenger {pid} updated successfully")

    # - TRIGGER (important)
    print(" Updating flight passenger status...")
    from passenger_allocation import allocate_passengers
    allocate_passengers()