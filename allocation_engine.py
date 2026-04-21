from aircraft import load_aircraft
from gates import load_gates
from runways import load_runways
from crew import load_crew
from ground_resources import load_resources
from data_loader import load_flights

# ---------------- LOAD EXISTING ALLOCATIONS ----------------
def load_allocations():

    alloc = {}

    try:
        with open("flight_allocations.txt") as f:
            for line in f:
                data = line.strip().split(",")
                alloc[data[0]] = data
    except:
        pass

    return alloc


# ---------------- SAVE ----------------
def save_allocation(fno, aircraft, gate, runway, crew_ids, resources):

    with open("flight_allocations.txt", "a") as f:
        f.write(
            f"{fno},{aircraft},{gate},{runway},{'|'.join(crew_ids)},{'|'.join(resources)}\n"
        )


# ---------------- UPDATE FILE HELPERS ----------------
def update_gate_file(gates):
    with open("gates.txt", "w") as f:
        for g in gates:
            f.write(",".join([
                g.gate_id, g.terminal,
                g.gate_type, g.max_aircraft_size,
                g.availability
            ]) + "\n")


def update_runway_file(runways):
    with open("runwaydetails.txt", "w") as f:
        for r in runways:
            f.write(",".join([
                str(r.length), r.availability,
                r.assigned_flight, r.runway_id,
                r.usage, r.maintenance_window,
                r.maintenance_from, r.maintenance_to
            ]) + "\n")


def update_crew_file(crew_list):
    with open("crew.txt", "w") as f:
        for c in crew_list:
            f.write(",".join([
                c.crew_id, c.name, c.role,
                c.flight_no, c.shift,
                c.aircraft_type, c.status,
                c.duty_hours, c.rest_hours
            ]) + "\n")


def update_resource_file(resources):
    with open("ground_resources.txt", "w") as f:
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


# ---------------- GATE (GREEDY) ----------------
def get_available_gate(flight, gates):

    for g in gates:

        if g.availability != "Free":
            continue

        # aircraft size check
        if g.max_aircraft_size != flight.aircraft_type:
            continue

        # international restriction
        if flight.flight_type == "International" and g.gate_type != "International":
            continue

        return g

    return None


# ---------------- RUNWAY (FIRST-FIT) ----------------
def get_available_runway(runways):

    for r in runways:

        if r.availability != "Free":
            continue

        if r.maintenance_window == "Yes":
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
def get_available_resources(resources):

    available = [r for r in resources if r.status == "Available"]

    if len(available) >= 2:
        return available[:2]

    return None

# ---------------- MAIN ALLOCATION ENGINE ----------------
def allocate_flight(flight):

    allocations = load_allocations()

    if flight.fno in allocations:
        print(" Already allocated")
        return

    aircraft_list = load_aircraft()
    gates = load_gates()
    runways = load_runways()
    crew_list = load_crew()
    resources = load_resources()
    flights = load_flights()

    new_arr = int(flight.arr)
    new_dep = int(flight.dep)

    # -------- AIRCRAFT --------
    aircraft = get_available_aircraft(flight, aircraft_list, flights)
    if not aircraft:
        print(" No aircraft available")
        return

    # -------- GATE --------
    selected_gate = None

    for g in gates:

        if g.availability != "Free":
            continue

        if g.max_aircraft_size != aircraft.atype:
            continue

        if getattr(flight, "flight_type", getattr(flight, "ftype", "Domestic")) == "International" and g.gate_type != "International":
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

        selected_gate = g
        break

    if not selected_gate:
        print(" No suitable gate available")
        return

    # -------- RUNWAY --------
    selected_runway = None

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

        selected_runway = r
        break

    if not selected_runway:
        print(" No runway available")
        return

    # -------- CREW --------
    selected_crew = []

    for c in crew_list:
        if c.status == "Available" and c.aircraft_type == aircraft.atype:
            selected_crew.append(c)

        if len(selected_crew) == 2:
            break

    if len(selected_crew) < 2:
        print(" Not enough crew")
        return

    # -------- RESOURCES --------
    selected_res = []

    for r in resources:
        if r.status == "Available":
            selected_res.append(r)

        if len(selected_res) == 2:
            break

    if len(selected_res) < 2:
        print(" Not enough resources")
        return

    # -------- FINAL UPDATE (ONLY AFTER FULL SUCCESS) --------
    selected_gate.availability = "Occupied"

    selected_runway.availability = "Occupied"
    selected_runway.assigned_flight = flight.fno

    flight.aircraft = aircraft.aircraft_id   

    for c in selected_crew:
        c.status = "Assigned"
        c.flight_no = flight.fno

    for r in selected_res:
        r.status = "In Use"

    # -------- SAVE TO FILES --------
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

def try_schedule_pending_flights():

    flights = load_flights()
    aircraft_list = load_aircraft()
    gates = load_gates()
    runways = load_runways()
    crew_list = load_crew()
    resources = load_resources()

    for flight in flights:

        # skip already allocated
        if flight.aircraft != "NA":
            continue

        allocate_flight(flight)

def auto_allocate_gate():

    from data_loader import load_flights

    flights = load_flights()

    for flight in flights:

        #  skip already allocated flights
        if flight.aircraft != "NA":
            continue

        allocate_flight(flight)

def allocate_aircraft(flight, aircraft_list, flights):

    for a in aircraft_list:

        #  skip aircraft under maintenance
        if a.maintenance == "Yes":
            continue

        #  skip if not at airport
        if a.location.lower() != "airport":
            continue

        conflict = False

        for f in flights:

            #  FIX: skip same flight (self-conflict bug)
            if f.fno == flight.fno:
                continue

            # check if same aircraft is used
            if f.aircraft == a.aircraft_id:

                existing_arr = int(f.arr)
                existing_dep = int(f.dep)

                #  overlap condition
                if not (int(flight.dep) <= existing_arr or int(flight.arr) >= existing_dep):
                    conflict = True
                    break

        # if no conflict → assign this aircraft
        if not conflict:
            return a

    # no aircraft found
    return None