# Class Runway to store info about runways

from validation import validate_runway
from constraint_checking import check_duplicate_runway, check_runway_maintenance_consistency


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

                length, availability, assigned_flight, runway_id, usage, maintenance_window, maintenance_from, maintenance_to = data

                # Field-level validation
                if not validate_runway(length, availability, usage, maintenance_window):
                    # validate_runway prints the error
                    continue

                # Maintenance consistency + duplicate checks
                if not check_runway_maintenance_consistency(maintenance_window, maintenance_from, maintenance_to):
                    continue

                if not check_duplicate_runway(runways, runway_id):
                    continue

                try:
                    runways.append(Runway(length, availability, assigned_flight, runway_id, usage, maintenance_window, maintenance_from, maintenance_to))
                except Exception as e:
                    print(f"Invalid runway entry skipped: {data} -> {e}")
                    continue

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


# Adding runways at runtime is not supported; runways are treated as static data.
def writeData():
    print("Runways are static; adding runways at runtime is not supported.")


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

    # validate prospective values first
    new_availability = availability if availability else target.availability
    new_usage = usage if usage else target.usage
    new_maintenance = maintenance if maintenance else target.maintenance_window

    if not validate_runway(str(target.length), new_availability, new_usage, new_maintenance):
        return

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