class Aircraft:

    def __init__(self, aid, atype, location, maintenance, tat):
        self.aircraft_id = aid
        self.atype = atype
        self.location = location
        self.maintenance = maintenance
        self.turnaround_time = int(tat)


# ---------------- LOAD ----------------
def load_aircraft():
    lst = []

    try:
        with open("aircraft.csv") as f:
            for line in f:
                data = line.strip().split(",")

                if len(data) != 5:
                    continue

                lst.append(Aircraft(*data))
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error loading aircraft: {e}")

    return lst


# ---------------- DISPLAY ----------------
def display_aircraft():

    aircraft_list = load_aircraft()

    if not aircraft_list:
        print("No aircraft available")
        return

    print("\n--- Aircraft ---")
    for a in aircraft_list:
        print(f"{a.aircraft_id} | {a.atype} | {a.location} | {a.maintenance} | TAT: {a.turnaround_time}")


# ---------------- WRITE ----------------
def writeData():

    n = int(input("Aircraft count: "))
    existing = load_aircraft()

    with open("aircraft.csv", "a") as f:

        for _ in range(n):

            aid = input("Aircraft ID: ")
            atype = input("Type (Wide/Narrow): ")
            location = input("Location (Airport/Other): ")
            maintenance = input("Maintenance (Yes/No): ")
            tat = input("Turnaround Time: ")

            if not tat.isdigit():
                print("Invalid turnaround time")
                continue

            if atype not in ["Wide", "Narrow"]:
                print("Invalid type. Must be Wide or Narrow")
                continue

            if maintenance not in ["Yes", "No"]:
                print("Invalid maintenance value. Must be Yes or No")
                continue

            if any(a.aircraft_id == aid for a in existing):
                print("Duplicate Aircraft ID")
                continue

            f.write(",".join([aid, atype, location, maintenance, tat]) + "\n")
            existing.append(Aircraft(aid, atype, location, maintenance, tat))

    print("✅ Aircraft added")

    from allocation_engine import try_schedule_pending_flights
    try_schedule_pending_flights()


# ---------------- UPDATE ----------------
def update_aircraft():

    aircraft_list = load_aircraft()

    if not aircraft_list:
        print("No aircraft available")
        return

    aid = input("Enter Aircraft ID to update: ")

    target = next((a for a in aircraft_list if a.aircraft_id == aid), None)

    if not target:
        print("Aircraft not found")
        return

    print(f"\nCurrent: {target.aircraft_id} | {target.atype} | {target.location} | {target.maintenance} | TAT: {target.turnaround_time}")
    print("Leave blank to keep current value\n")

    atype = input(f"Type (Wide/Narrow) [{target.atype}]: ").strip()
    location = input(f"Location (Airport/Other) [{target.location}]: ").strip()
    maintenance = input(f"Maintenance (Yes/No) [{target.maintenance}]: ").strip()
    tat = input(f"Turnaround Time [{target.turnaround_time}]: ").strip()

    # 🔹 APPLY CHANGES
    if atype:
        if atype not in ["Wide", "Narrow"]:
            print("Invalid type")
            return
        target.atype = atype

    if location:
        target.location = location

    if maintenance:
        if maintenance not in ["Yes", "No"]:
            print("Invalid maintenance value")
            return
        target.maintenance = maintenance

    if tat:
        if not tat.isdigit():
            print("Invalid turnaround time")
            return
        target.turnaround_time = int(tat)

    # 🔹 SAVE FILE
    with open("aircraft.csv", "w") as f:
        for a in aircraft_list:
            f.write(",".join([
                a.aircraft_id,
                a.atype,
                a.location,
                a.maintenance,
                str(a.turnaround_time)
            ]) + "\n")

    print(f"✅ Aircraft {aid} updated successfully")

    # 🔥 NEW CLEAN LOGIC

    from allocation_engine import load_allocations, remove_allocation_for_flight, try_schedule_pending_flights

    allocations = load_allocations()

    # ❗ If aircraft becomes unusable → FULL RESET
    if target.maintenance == "Yes" or target.location.lower() != "airport":

        affected_flights = []

        for fno, data in allocations.items():
            if len(data) >= 2 and data[1] == aid:
                affected_flights.append(fno)

        for fno in affected_flights:
            remove_allocation_for_flight(fno)

        if affected_flights:
            print(f"⚠️ Aircraft removed from flights: {affected_flights}")

    # ✅ If aircraft becomes usable → try allocation
    else:
        print("🔄 Trying to allocate pending flights...")
        try_schedule_pending_flights()
# ---------------- REMOVE ----------------
def remove_aircraft():

    aircraft_list = load_aircraft()

    if not aircraft_list:
        print("No aircraft available")
        return

    aid = input("Enter Aircraft ID to remove: ")

    target = next((a for a in aircraft_list if a.aircraft_id == aid), None)

    if not target:
        print("Aircraft not found")
        return

    # check if allocated
    try:
        with open("flight_allocations.csv") as f:
            for line in f:
                data = line.strip().split(",")
                if len(data) >= 2 and data[1] == aid:
                    print("❌ Cannot delete: Aircraft is allocated to a flight")
                    return
    except FileNotFoundError:
        pass

    updated = [a for a in aircraft_list if a.aircraft_id != aid]

    with open("aircraft.csv", "w") as f:
        for a in updated:
            f.write(",".join([
                a.aircraft_id,
                a.atype,
                a.location,
                a.maintenance,
                str(a.turnaround_time)
            ]) + "\n")

    print("✅ Aircraft removed successfully")