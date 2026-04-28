from aircraft import load_aircraft
from gates import load_gates
from runways import load_runways
from crew import load_crew
from ground_resources import load_resources



# ---------------- LOAD EXISTING ALLOCATIONS ----------------
def load_allocations():

    alloc = {}

    try:
        with open("flight_allocations.csv") as f:
            for line in f:
                data = line.strip().split(",")
                if len(data) >= 4:
                    alloc[data[0]] = data
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error loading allocations: {e}")

    return alloc


# ---------------- SAVE ALLOCATION ----------------
def save_allocation(fno, aircraft, gate, runway, crew_ids, resources):

    with open("flight_allocations.csv", "a") as f:
        f.write(
            f"{fno},{aircraft},{gate},{runway},{'|'.join(crew_ids)},{'|'.join(resources)}\n"
        )


# ---------------- UPDATE FILE HELPERS ----------------
def update_flight_file(flights):
    with open("flights.csv", "w") as f:
        for fl in flights:
            f.write(",".join([
                fl.fno, fl.airline, fl.origin, fl.destination,
                fl.arr, fl.dep, fl.date, fl.aircraft, fl.flight_type, str(fl.capacity)
            ]) + "\n")


def update_gate_file(gates):
    with open("gates.csv", "w") as f:
        for g in gates:
            f.write(",".join([
                g.gate_id, g.terminal,
                g.gate_type, g.max_aircraft_size,
                g.availability
            ]) + "\n")


def update_runway_file(runways):
    with open("runwaydetails.csv", "w") as f:
        for r in runways:
            f.write(",".join([
                str(r.length), r.availability,
                r.assigned_flight, r.runway_id,
                r.usage, r.maintenance_window,
                r.maintenance_from, r.maintenance_to
            ]) + "\n")


def update_crew_file(crew_list):
    with open("crew.csv", "w") as f:
        for c in crew_list:
            f.write(",".join([
                c.crew_id, c.name, c.role,
                c.flight_no, c.shift,
                c.aircraft_type, c.status,
                c.duty_hours, c.rest_hours
            ]) + "\n")


def update_resource_file(resources):
    with open("ground_resources.csv", "w") as f:
        for r in resources:
            f.write(",".join([
                r.res_id, r.res_type, r.status
            ]) + "\n")


# ---------------- AIRCRAFT (TIME-BASED VALIDATION) ----------------
def get_available_aircraft(flight, aircraft_list, flights):

    for a in aircraft_list:

        if a.maintenance == "Yes":
            continue

        if a.location.lower() != "airport":
            continue

        conflict = False

        for f in flights:

            if f.fno == flight.fno:
                continue

            if f.aircraft == a.aircraft_id:

                existing_arr = int(f.arr)
                existing_dep = int(f.dep)

                if not (int(flight.dep) <= existing_arr or int(flight.arr) >= existing_dep):
                    conflict = True
                    break

        if not conflict:
            return a

    return None


# ---------------- GATE (GREEDY + TIME CHECK) ----------------
def get_available_gate(flight, gates, allocations, flights, aircraft):

    new_arr = int(flight.arr)
    new_dep = int(flight.dep)

    for g in gates:

        if g.availability != "Free":
            continue

        if g.max_aircraft_size != aircraft.atype:
            continue

        flight_type = flight.flight_type
        if flight_type == "International" and g.gate_type != "International":
            continue

        conflict = False

        for f in flights:
            if f.fno == flight.fno:
                continue

            if f.fno in allocations:
                alloc_data = allocations[f.fno]
                used_gate = alloc_data[2]

                if used_gate == g.gate_id:
                    existing_arr = int(f.arr)
                    existing_dep = int(f.dep)

                    if not (new_dep <= existing_arr or new_arr >= existing_dep):
                        conflict = True
                        break

        if conflict:
            continue

        return g

    return None


# ---------------- RUNWAY (FIRST-FIT + TIME CHECK) ----------------
def get_available_runway(flight, runways, allocations, flights):

    new_arr = int(flight.arr)
    new_dep = int(flight.dep)

    for r in runways:

        if r.availability != "Free":
            continue

        if r.maintenance_window == "Yes":
        
            continue

        conflict = False

        for f in flights:
            if f.fno == flight.fno:
                continue

            if f.fno in allocations:
                alloc_data = allocations[f.fno]
                used_runway = alloc_data[3]

                if used_runway == r.runway_id:
                    existing_arr = int(f.arr)
                    existing_dep = int(f.dep)

                    if not (new_dep <= existing_arr or new_arr >= existing_dep):
                        conflict = True
                        break

        if conflict:
            continue

        return r

    return None


# ---------------- CREW (CSP LIGHT) ----------------
def get_available_crew(crew_list, aircraft_type):

    valid = [
        c for c in crew_list
        if c.status == "Available" and c.aircraft_type == aircraft_type
    ]

    if len(valid) >= 2:
        return valid[:2]

    return None


# ---------------- RESOURCE (GREEDY) ----------------
def get_available_resources(resources, allocations, interactive=False):

    selected = []

    for r in resources:

        #  CASE 1: Available → take directly
        if r.status == "Available":
            selected.append(r)

        #  CASE 2: In Use → ask user (only if interactive mode ON)
        elif r.status == "In Use" and interactive:

            used_by = None

            # 🔍 find which flight is using this resource
            for fno, data in allocations.items():
                if len(data) > 5 and r.res_id in data[5].split("|"):
                    used_by = fno
                    break

            print(f" Resource {r.res_id} is currently used by Flight {used_by}")

            choice = input("Do you want to reassign it? (yes/no): ")

            if choice.lower() == "yes":

                from allocation_engine import remove_allocation_for_flight
                remove_allocation_for_flight(used_by)

                selected.append(r)

        # stop when enough resources collected
        if len(selected) == 2:
            break

    if len(selected) < 2:
        return None

    return selected


# ---------------- MAIN ALLOCATION ENGINE ----------------
def allocate_flight(flight):
    from flights import load_flights
    allocations = load_allocations()

    if flight.fno in allocations:
        print(f"Flight {flight.fno} already allocated")
        return

    aircraft_list = load_aircraft()
    gates = load_gates()
    runways = load_runways()
    crew_list = load_crew()
    resources = load_resources()
    flights = load_flights()

    # -------- AIRCRAFT --------
    aircraft = get_available_aircraft(flight, aircraft_list, flights)
    if not aircraft:
        print(f" No aircraft available for flight {flight.fno}")
        return

    # -------- GATE --------
    selected_gate = get_available_gate(flight, gates, allocations, flights, aircraft)
    if not selected_gate:
        print(f" No suitable gate available for flight {flight.fno}")
        return

    # -------- RUNWAY --------
    selected_runway = get_available_runway(flight, runways, allocations, flights)
    if not selected_runway:
        print(f" No runway available for flight {flight.fno}")
        return

    # -------- CREW --------
    selected_crew = get_available_crew(crew_list, aircraft.atype)
    if not selected_crew:
        print(f" Not enough crew for flight {flight.fno}")
        return

    # -------- RESOURCES --------
    selected_res = get_available_resources(resources, allocations, interactive=False)
    if not selected_res:
        print(f" Not enough resources for flight {flight.fno}")
        return

    # -------- FINAL UPDATE (ONLY AFTER FULL SUCCESS) --------
    selected_gate.availability = "Occupied"

    selected_runway.availability = "Occupied"
    selected_runway.assigned_flight = flight.fno

    for c in selected_crew:
        c.status = "Assigned"
        c.flight_no = flight.fno

    for r in selected_res:
        r.status = "In Use"

    # update aircraft field on flight object and persist to file
    flight.aircraft = aircraft.aircraft_id
    for fl in flights:
        if fl.fno == flight.fno:
            fl.aircraft = aircraft.aircraft_id
            break
    update_flight_file(flights)

    # -------- SAVE ALL FILES --------
    update_gate_file(gates)
    update_runway_file(runways)
    update_crew_file(crew_list)
    update_resource_file(resources)

    save_allocation(
        flight.fno,
        aircraft.aircraft_id,
        selected_gate.gate_id,
        selected_runway.runway_id,
        [c.crew_id for c in selected_crew],
        [r.res_id for r in selected_res]
    )

    print(f" Flight {flight.fno} fully allocated")
    print(f"   Aircraft : {aircraft.aircraft_id}")
    print(f"   Gate     : {selected_gate.gate_id}")
    print(f"   Runway   : {selected_runway.runway_id}")
    print(f"   Crew     : {[c.crew_id for c in selected_crew]}")
    print(f"   Resources: {[r.res_id for r in selected_res]}")

    print(" Trigger: Allocation successful → System state updated")


# ---------------- SCHEDULE PENDING FLIGHTS ----------------
def try_schedule_pending_flights():
    from flights import load_flights
    flights = load_flights()

    pending = [f for f in flights if f.aircraft == "NA"]

    if not pending:
        print("No pending flights to allocate")
        return

    print(f"\n Found {len(pending)} pending flight(s). Attempting allocation...")

    for flight in pending:
        allocate_flight(flight)


def remove_allocation_for_flight(fno):

    allocations = load_allocations()

    if fno not in allocations:
        print("No allocation found for this flight")
        return

    data = allocations[fno]

    gate_id = data[2]
    runway_id = data[3]
    crew_ids = data[4].split("|") if len(data) > 4 else []
    res_ids = data[5].split("|") if len(data) > 5 else []

    gates = load_gates()
    runways = load_runways()
    crew_list = load_crew()
    resources = load_resources()

    # FREE GATE
    for g in gates:
        if g.gate_id == gate_id:
            g.availability = "Free"

    # FREE RUNWAY
    for r in runways:
        if r.runway_id == runway_id:
            r.availability = "Free"
            r.assigned_flight = "NA"

    # FREE CREW
    for c in crew_list:
        if c.crew_id in crew_ids:
            c.status = "Available"
            c.flight_no = "NA"

    # FREE RESOURCES
    for r in resources:
        if r.res_id in res_ids:
            r.status = "Available"

    # UPDATE FILES
    update_gate_file(gates)
    update_runway_file(runways)
    update_crew_file(crew_list)
    update_resource_file(resources)

    # REMOVE FROM FILE
    with open("flight_allocations.csv", "r") as f:
        lines = f.readlines()

    with open("flight_allocations.csv", "w") as f:
        for line in lines:
            if not line.startswith(fno + ","):
                f.write(line)

    print(f" Allocation for flight {fno} removed")

    print(" Trigger: Resources released → Reallocation triggered")

   
    try_schedule_pending_flights()