from validation import validate_gate
from constraint_checking import check_duplicate_gate


class Gate:

    def __init__(self, gid, terminal, gtype, size, availability):
        self.gate_id = gid
        self.terminal = terminal
        self.gate_type = gtype
        self.max_aircraft_size = size
        self.availability = availability


# ---------------- LOAD ----------------
def load_gates():
    lst = []

    try:
        with open("gates.csv") as f:
            for line in f:
                data = line.strip().split(',')

                if len(data) != 5:
                    continue

                gid, terminal, gtype, size, availability = data

                # Field-level validation
                if not validate_gate(gid, gtype, size, availability):
                    continue

                # Duplicate check
                from constraint_checking import check_duplicate_gate
                if not check_duplicate_gate(lst, gid):
                    continue

                try:
                    lst.append(Gate(gid, terminal, gtype, size, availability))
                except Exception:
                    print("Invalid gate entry skipped:", data)
                    continue
    except FileNotFoundError:
        pass

    return lst


# ---------------- DISPLAY ----------------
def display_gates():

    gates = load_gates()

    if not gates:
        print("No gates available")
        return

    print("\n--- Gates ---")
    for g in gates:
        print(f"{g.gate_id} | {g.terminal} | {g.gate_type} | {g.max_aircraft_size} | {g.availability}")


# ---------------- WRITE ----------------
def writeData():
    print("Gates are static; adding gates at runtime is not supported.")


# ---------------- REMOVE ----------------
def remove_gate():

    gid = input("Enter Gate ID to remove: ")

    gates = load_gates()
    updated = []

    found = False

    # - check allocations
    from allocation_engine import load_allocations
    allocations = load_allocations()

    for g in gates:

        if g.gate_id == gid:
            found = True

            # - If gate is used → remove entire allocation (same philosophy)
            for fno, data in allocations.items():
                if len(data) > 2 and data[2] == gid:
                    print(f"- Gate used by flight {fno} → removing allocation")

                    from allocation_engine import remove_allocation_for_flight
                    remove_allocation_for_flight(fno)

            continue

        updated.append(g)

    if not found:
        print(" Gate not found")
        return

    #  SAVE FILE
    with open("gates.csv", "w") as f:
        for g in updated:
            f.write(",".join([
                g.gate_id, g.terminal,
                g.gate_type, g.max_aircraft_size,
                g.availability
            ]) + "\n")

    print(" Gate removed successfully")

    #  TRIGGER
    print("- Reallocating pending flights...")
    from allocation_engine import system_rebalance
    system_rebalance()


# ---------------- UPDATE ----------------
def update_gate():

    gates = load_gates()

    if not gates:
        print("No gates available")
        return

    gid = input("Enter Gate ID to update: ")

    target = next((g for g in gates if g.gate_id == gid), None)

    if not target:
        print("Gate not found")
        return

    print(f"\nCurrent: {target.gate_id} | {target.terminal} | {target.gate_type} | {target.max_aircraft_size} | {target.availability}")
    print("Leave blank to keep current value\n")

    terminal = input(f"Terminal [{target.terminal}]: ").strip()
    gtype = input(f"Type [{target.gate_type}]: ").strip()
    size = input(f"Size [{target.max_aircraft_size}]: ").strip()
    availability = input(f"Availability [{target.availability}]: ").strip()

    old_availability = target.availability

    # - APPLY CHANGES: validate prospective values first
    new_gtype = gtype if gtype else target.gate_type
    new_size = size if size else target.max_aircraft_size
    new_availability = availability if availability else target.availability

    if not validate_gate(target.gate_id, new_gtype, new_size, new_availability):
        return

    if terminal:
        target.terminal = terminal

    if gtype:
        target.gate_type = gtype

    if size:
        target.max_aircraft_size = size

    if availability:
        target.availability = availability

    # - SAVE FILE
    with open("gates.csv", "w") as f:
        for g in gates:
            f.write(",".join([
                g.gate_id,
                g.terminal,
                g.gate_type,
                g.max_aircraft_size,
                g.availability
            ]) + "\n")

    print(f"- Gate {gid} updated successfully")

    # - SMART TRIGGER (same logic as aircraft)

    # - Became FREE → rebalance system
    if target.availability == "Free" and old_availability != "Free":
        print(" Gate became free → triggering system rebalance")

        from allocation_engine import system_rebalance
        system_rebalance()

    # - Became OCCUPIED manually → reset system safely
    elif target.availability != "Free" and old_availability == "Free":
        print(" Gate manually occupied → resetting allocations")

        from allocation_engine import load_allocations, remove_allocation_for_flight, system_rebalance

        allocations = load_allocations()

        for fno, data in allocations.items():
            if len(data) > 2 and data[2] == gid:
                remove_allocation_for_flight(fno, auto_reallocate=False)

        system_rebalance()