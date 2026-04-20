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
        with open("aircraft.txt") as f:
            for line in f:
                data = line.strip().split(",")

                if len(data) != 5:
                    continue

                lst.append(Aircraft(*data))
    except:
        pass

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

    with open("aircraft.txt", "a") as f:

        for _ in range(n):

            aid = input("Aircraft ID: ")
            atype = input("Type (Wide/Narrow): ")
            location = input("Location (Airport/Other): ")
            maintenance = input("Maintenance (Yes/No): ")
            tat = input("Turnaround Time: ")

            if not tat.isdigit():
                print("Invalid turnaround time")
                continue

            if any(a.aircraft_id == aid for a in existing):
                print("Duplicate Aircraft ID")
                continue

            f.write(",".join([aid, atype, location, maintenance, tat]) + "\n")

            existing.append(Aircraft(aid, atype, location, maintenance, tat))

    print("✅ Aircraft added")