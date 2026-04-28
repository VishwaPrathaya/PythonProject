from validation import validate_crew
from constraint_checking import check_crew_constraints


class Crew:

    def __init__(self, cid, name, role, fno, shift, atype, status, duty_hours, rest_hours):

        self.crew_id = cid
        self.name = name
        self.role = role
        self.flight_no = fno
        self.shift = shift
        self.aircraft_type = atype
        self.status = status
        self.duty_hours = duty_hours
        self.rest_hours = rest_hours


def load_crew():
    lst = []
    try:
        with open("crew.csv") as f:
            for line in f:
                data = line.strip().split(",")
                if len(data) == 9:
                    lst.append(Crew(*data))
    except:
        pass
    return lst

def display_crew():
    records = load_crew()

    if not records:
        print("\nNo crew data available.")
        return

    for i in records:
        print("\n===== CREW DETAILS =====")
        print("Crew ID        :", i.crew_id)
        print("Name           :", i.name)
        print("Role           :", i.role)
        print("Flight No      :", i.flight_no)
        print("Shift          :", i.shift)
        print("Aircraft Type  :", i.aircraft_type)
        print("Status         :", i.status)
        print("-----------------------------")

def writeData():

    n = int(input("Crew count: "))
    records = load_crew()   # optional for duplicate check

    with open("crew.csv", "a") as f:

        for _ in range(n):

            cid = input("ID: ")
            name = input("Name: ")
            role = input("Role: ")
            fno = input("Flight: ")
            shift = input("Shift: ")

            if not validate_crew(cid, name, role):
                continue

            atype = input("Aircraft Type: ")
            status = input("Status: ")

            duty = input("Duty Hours: ")
            rest = input("Rest Hours: ")

            # 🔹 simple validation only
            if not duty.isdigit() or not rest.isdigit():
                print("Duty/Rest must be numbers")
                continue

            # optional duplicate check
            if any(c.crew_id == cid for c in records):
                print("Duplicate Crew ID")
                continue

            f.write(",".join([
                cid, name, role, fno, shift,
                atype, status, duty, rest
            ]) + "\n")

            records.append(Crew(
                cid, name, role, fno, shift,
                atype, status, duty, rest
            ))


def remove_crew():

    crew_list = load_crew()

    if not crew_list:
        print("No crew available")
        return

    cid = input("Enter Crew ID to remove: ")

    #  check existence
    found = False
    for c in crew_list:
        if c.crew_id == cid:
            found = True
            break

    if not found:
        print("Crew not found")
        return

    #  check allocation file
    try:
        with open("flight_allocations.csv") as f:
            for line in f:
                data = line.strip().split(",")

                if len(data) >= 5:
                    crew_ids = data[4].split("|")

                    if cid in crew_ids:
                        print(" Cannot remove: Crew is assigned to a flight")
                        return
    except:
        pass

    #  remove crew
    updated = [c for c in crew_list if c.crew_id != cid]

    with open("crew.csv", "w") as f:
        for c in updated:
            f.write(",".join([
                c.crew_id, c.name, c.role,
                c.flight_no, c.shift,
                c.aircraft_type, c.status,
                c.duty_hours, c.rest_hours
            ]) + "\n")

    print(" Crew removed successfully")

# ---------------- UPDATE ----------------
def update_crew():

    crew_list = load_crew()

    if not crew_list:
        print("No crew available")
        return

    cid = input("Enter Crew ID to update: ")

    target = next((c for c in crew_list if c.crew_id == cid), None)

    if not target:
        print("Crew not found")
        return

    print(f"\nCurrent: {target.crew_id} | {target.name} | {target.role} | {target.status}")
    print("Leave blank to keep current value\n")

    name = input(f"Name [{target.name}]: ").strip()
    role = input(f"Role [{target.role}]: ").strip()
    atype = input(f"Aircraft Type [{target.aircraft_type}]: ").strip()
    status = input(f"Status [{target.status}]: ").strip()
    duty = input(f"Duty Hours [{target.duty_hours}]: ").strip()
    rest = input(f"Rest Hours [{target.rest_hours}]: ").strip()

    if name:
        target.name = name

    if role:
        target.role = role

    if atype:
        target.aircraft_type = atype

    if status:
        target.status = status

    if duty:
        if not duty.isdigit():
            print("Invalid duty hours")
            return
        target.duty_hours = duty

    if rest:
        if not rest.isdigit():
            print("Invalid rest hours")
            return
        target.rest_hours = rest

    #  SAVE FILE
    with open("crew.csv", "w") as f:
        for c in crew_list:
            f.write(",".join([
                c.crew_id, c.name, c.role,
                c.flight_no, c.shift,
                c.aircraft_type, c.status,
                c.duty_hours, c.rest_hours
            ]) + "\n")

    print(f" Crew {cid} updated successfully")

    

    from allocation_engine import load_allocations, remove_allocation_for_flight, try_schedule_pending_flights

    allocations = load_allocations()

    # CASE 1: Crew becomes AVAILABLE → try allocation
    if target.status == "Available":
        print(" Crew available → trying to allocate pending flights...")
        try_schedule_pending_flights()

    # CASE 2: Crew becomes UNAVAILABLE → remove full allocations
    else:
        affected = []

        for fno, data in allocations.items():
            if len(data) >= 5:
                crew_ids = data[4].split("|")

                if cid in crew_ids:
                    affected.append(fno)

        for fno in affected:
            print(f" Removing full allocation for flight {fno}")
            remove_allocation_for_flight(fno)
