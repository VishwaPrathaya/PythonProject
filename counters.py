from validation import validate_counter
from constraint_checking import check_duplicate_counter


class Counter:

    def __init__(self, counter_id, gate_id, terminal, service_type, availability, capacity=50):
        self.counter_id = counter_id
        self.gate_id = gate_id
        self.terminal = terminal
        self.service_type = service_type
        self.availability = availability
        self.capacity = int(capacity)


# ---------------- LOAD ----------------
def load_counters():
    counters = []

    try:
        with open("counters.csv", "r") as f:
            for line in f:
                data = line.strip().split(",")
                if len(data) not in [5, 6]:
                    continue

                if len(data) == 5:
                    cid, gate_id, terminal, service_type, availability = data
                    capacity = 50
                else:
                    cid, gate_id, terminal, service_type, availability, capacity = data

                if not validate_counter(cid, gate_id, terminal, service_type, availability):
                    continue

                if not check_duplicate_counter(counters, cid):
                    continue

                counters.append(Counter(cid, gate_id, terminal, service_type, availability, capacity))
    except FileNotFoundError:
        pass

    return counters


# ---------------- DISPLAY ----------------
def display_counters():
    counters = load_counters()

    if not counters:
        print("No counters available")
        return

    print("\n--- Counters ---")
    for c in counters:
        print(f"{c.counter_id} | Gate: {c.gate_id} | Terminal: {c.terminal} | {c.service_type} | {c.availability} | Capacity: {c.capacity}")


# ---------------- WRITE ----------------
def writeData():
    print("\n===== Counter Management Module =====")

    n = int(input("Enter number of counters to add: "))
    existing = load_counters()
    new_added = False

    with open("counters.csv", "a") as f:
        for i in range(n):
            print(f"\nCounter {i + 1}")
            cid = input("Counter ID: ").strip()
            gate_id = input("Gate ID: ").strip()
            terminal = input("Terminal: ").strip()
            service_type = input("Service Type (Check-In/Boarding): ").strip()
            availability = input("Availability (Available/Occupied): ").strip()
            capacity = input("Capacity (default 50): ").strip() or "50"

            if not validate_counter(cid, gate_id, terminal, service_type, availability):
                print("Invalid counter specification. Skipping.")
                continue

            if not capacity.isdigit():
                print("Invalid capacity. Skipping.")
                continue

            if not check_duplicate_counter(existing, cid):
                print("Duplicate counter ID. Skipping.")
                continue

            counter = Counter(cid, gate_id, terminal, service_type, availability, capacity)
            existing.append(counter)
            f.write(",".join([cid, gate_id, terminal, service_type, availability, str(counter.capacity)]) + "\n")
            print(f"Counter {cid} added.")
            new_added = True

    if new_added:
        print("- New counters available → reallocating pending flights")
        from allocation_engine import try_schedule_pending_flights
        try_schedule_pending_flights()


def add_counter():
    """Add one or more counters when passenger demand is high."""
    writeData()


def create_counter(counter_id, gate_id, terminal, service_type, availability, capacity=50):
    """Programmatically create a counter and persist it to counters.csv.

    Returns the created Counter object or None if creation failed.
    """
    existing = load_counters()

    if not validate_counter(counter_id, gate_id, terminal, service_type, availability):
        return None

    if not check_duplicate_counter(existing, counter_id):
        return None

    counter = Counter(counter_id, gate_id, terminal, service_type, availability, capacity)

    with open("counters.csv", "a") as f:
        f.write(",".join([counter.counter_id, counter.gate_id, counter.terminal, counter.service_type, counter.availability, str(counter.capacity)]) + "\n")

    return counter


# ---------------- REMOVE ----------------
def remove_counter():
    cid = input("Enter Counter ID to remove: ").strip()
    counters = load_counters()
    updated = []
    found = False

    for c in counters:
        if c.counter_id == cid:
            found = True
            continue
        updated.append(c)

    if not found:
        print("Counter not found")
        return

    with open("counters.csv", "w") as f:
        for c in updated:
            f.write(",".join([c.counter_id, c.gate_id, c.terminal, c.service_type, c.availability, str(c.capacity)]) + "\n")

    print(f"Counter {cid} removed successfully")
    print("- Reallocating pending flights...")
    from allocation_engine import try_schedule_pending_flights
    try_schedule_pending_flights()


# ---------------- UPDATE ----------------
def update_counter():
    counters = load_counters()

    if not counters:
        print("No counters available")
        return

    cid = input("Enter Counter ID to update: ").strip()
    target = next((c for c in counters if c.counter_id == cid), None)

    if not target:
        print("Counter not found")
        return

    print(f"\nCurrent: {target.counter_id} | Gate: {target.gate_id} | Terminal: {target.terminal} | {target.service_type} | {target.availability}")
    print("Leave blank to keep current value\n")

    gate_id = input(f"Gate ID [{target.gate_id}]: ").strip()
    terminal = input(f"Terminal [{target.terminal}]: ").strip()
    service_type = input(f"Service Type [{target.service_type}]: ").strip()
    availability = input(f"Availability [{target.availability}]: ").strip()

    if gate_id:
        target.gate_id = gate_id
    if terminal:
        target.terminal = terminal
    if service_type:
        target.service_type = service_type
    old_availability = target.availability

    if availability:
        target.availability = availability

    if not validate_counter(target.counter_id, target.gate_id, target.terminal, target.service_type, target.availability):
        print("Updated values are invalid. Update aborted.")
        return

    with open("counters.csv", "w") as f:
        for c in counters:
            f.write(",".join([c.counter_id, c.gate_id, c.terminal, c.service_type, c.availability, str(c.capacity)]) + "\n")

    print(f"Counter {cid} updated successfully")

    from allocation_engine import load_allocations, remove_allocation_for_flight, try_schedule_pending_flights
    allocations = load_allocations()

    if target.availability != "Available" and old_availability == "Available":
        print(" Counter unavailable → releasing affected allocations")
        for fno, data in allocations.items():
            if len(data) >= 7:
                counter_ids = data[6].split("|")
                if cid in counter_ids:
                    remove_allocation_for_flight(fno)
        print("- Reallocating pending flights...")
        try_schedule_pending_flights()
    else:
        print("- Reallocating pending flights...")
        try_schedule_pending_flights()


# ---------------- HELPERS ----------------
def get_available_counters(gate_id, counters):
    return [c for c in counters if c.gate_id == gate_id and c.availability == "Available"]


def update_counter_file(counters):
    with open("counters.csv", "w") as f:
        for c in counters:
            f.write(",".join([c.counter_id, c.gate_id, c.terminal, c.service_type, c.availability, str(c.capacity)]) + "\n")
