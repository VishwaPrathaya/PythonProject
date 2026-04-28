# Class Runway to store info about runways

from validation import validate_runway


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


# ---------------- LOAD ----------------
def load_runways():

    runways = []

    try:
        with open("runwaydetails.csv", "r") as f:

            for line in f:
                data = line.strip().split(",")

                if len(data) != 8:
                    continue

                runways.append(Runway(*data))

    except FileNotFoundError:
        pass

    return runways


# ---------------- DISPLAY ----------------
def display_runways():

    runways = load_runways()

    if not runways:
        print("\nNo runway data available.")
        return

    print("\n--- Runway Details ---")

    for r in runways:
        print(f"{r.runway_id} | {r.length} | {r.availability} | {r.assigned_flight} | {r.usage} | {r.maintenance_window}")


# ---------------- WRITE ----------------
def writeData():

    print("Runway Module")
    n = int(input("Enter number of runways: "))
    existing = load_runways()

    new_added = False

    with open("runwaydetails.csv", "a") as file:

        for _ in range(n):

            runway_id = input("Runway ID: ")
            length = input("Length: ")
            availability = input("Availability (Free/Occupied): ")
            assigned_flight = "NA"
            usage = input("Usage (Takeoff/Landing/Both): ")
            maintenance_window = input("Maintenance (Yes/No): ")
            maintenance_from = input("From (NA if none): ")
            maintenance_to = input("To (NA if none): ")

            if not validate_runway(length, availability, usage, maintenance_window):
                continue

            if any(r.runway_id == runway_id for r in existing):
                print("Duplicate runway")
                continue

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

            new_added = True

    print("- Runways added")

    # - SAME AS AIRCRAFT / GATE
    if new_added:
        from allocation_engine import try_schedule_pending_flights
        try_schedule_pending_flights()


# ---------------- REMOVE ----------------
def remove_runway():

    rid = input("Enter Runway ID to remove: ")

    runways = load_runways()
    updated = []

    found = False

    from allocation_engine import load_allocations
    allocations = load_allocations()

    for r in runways:

        if r.runway_id == rid:
            found = True

            # - DIRECT DEALLOCATION 
            for fno, data in allocations.items():

                if len(data) > 3 and data[3] == rid:
                    print(f"- Runway used by Flight {fno} → removing allocation")

                    from allocation_engine import remove_allocation_for_flight
                    remove_allocation_for_flight(fno)

            continue

        updated.append(r)

    if not found:
        print("- Runway not found")
        return

    with open("runwaydetails.csv", "w") as f:
        for r in updated:
            f.write(",".join([
                str(r.length), r.availability,
                r.assigned_flight, r.runway_id,
                r.usage, r.maintenance_window,
                r.maintenance_from, r.maintenance_to
            ]) + "\n")

    print("- Runway removed successfully")

    # - RE-ALLOCATE
    from allocation_engine import try_schedule_pending_flights
    try_schedule_pending_flights()


# ---------------- UPDATE ----------------
def update_runway():

    runways = load_runways()

    if not runways:
        print("No runways available")
        return

    rid = input("Enter Runway ID to update: ")

    target = next((r for r in runways if r.runway_id == rid), None)

    if not target:
        print("Runway not found")
        return

    print(f"\nCurrent: {target.runway_id} | {target.availability} | {target.maintenance_window}")
    print("Leave blank to keep current value\n")

    availability = input(f"Availability [{target.availability}]: ").strip()
    usage = input(f"Usage [{target.usage}]: ").strip()
    maintenance = input(f"Maintenance [{target.maintenance_window}]: ").strip()

    if availability:
        target.availability = availability

    if usage:
        target.usage = usage

    if maintenance:
        target.maintenance_window = maintenance

    # - SAVE FILE
    with open("runwaydetails.csv", "w") as f:
        for r in runways:
            f.write(",".join([
                str(r.length), r.availability,
                r.assigned_flight, r.runway_id,
                r.usage, r.maintenance_window,
                r.maintenance_from, r.maintenance_to
            ]) + "\n")

    print(f"- Runway {rid} updated successfully")

    # - SAME DESIGN PATTERN (NO RELEASE FUNCTION)
    if target.availability == "Free" and target.maintenance_window == "No":
        print("- Runway available → reallocating flights")
        from allocation_engine import try_schedule_pending_flights
        try_schedule_pending_flights()

    else:
        print("- Runway unavailable → affected flights will be reprocessed")
        from allocation_engine import try_schedule_pending_flights
        try_schedule_pending_flights()