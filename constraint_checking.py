# Constraint Checking Module

last_constraint_error = None

def get_last_constraint_error():
    return last_constraint_error

# -------------------- FLIGHT --------------------
def validate_flight_constraints(flight_list, flight_no, arrival, departure):
    global last_constraint_error
    last_constraint_error = None

    # duplicate safety (extra layer)
    for f in flight_list:
        if f.fno == flight_no:
            last_constraint_error = "Flight already exists"
            print(last_constraint_error)
            return False

    if arrival >= departure:
        last_constraint_error = "Invalid schedule"
        print(last_constraint_error)
        return False

    return True


# -------------------- PASSENGER --------------------
def check_passenger_constraints(passenger_list, flight_no, seat_no, capacity):

    count = 0

    global last_constraint_error
    last_constraint_error = None
    for p in passenger_list:

        if p.flight_no == flight_no:
            count += 1

            if p.seat_no == seat_no:
                last_constraint_error = "Seat already booked"
                print(last_constraint_error)
                return False

    if count >= capacity:
        last_constraint_error = "Flight full"
        print(last_constraint_error)
        return False

    return True


# -------------------- DISRUPTION --------------------
def check_disruption_constraints(dtype, status):
    global last_constraint_error
    last_constraint_error = None

    if dtype not in ["Delay", "Technical", "Weather"]:
        last_constraint_error = "Invalid type"
        print(last_constraint_error)
        return False

    if status not in ["Resolved", "Pending"]:
        last_constraint_error = "Invalid status"
        print(last_constraint_error)
        return False

    return True

# ---------------- AIRCRAFT ----------------
def check_aircraft_constraints(aircraft_list, flight_list, aircraft_id, new_arr, new_dep):
    global last_constraint_error
    last_constraint_error = None

    aircraft = next((a for a in aircraft_list if a.aircraft_id == aircraft_id), None)

    if not aircraft:
        last_constraint_error = "Aircraft not found"
        print(last_constraint_error)
        return False

    if aircraft.maintenance.lower() == "yes":
        last_constraint_error = "Aircraft under maintenance"
        print(last_constraint_error)
        return False

    if aircraft.location.lower() != "airport":
        last_constraint_error = "Aircraft not at airport"
        print(last_constraint_error)
        return False

    tat = aircraft.turnaround_time

    for f in flight_list:

        if f.aircraft != aircraft_id:
            continue

        existing_arr = int(f.arr)
        existing_dep = int(f.dep)

        # overlap check
        if not (new_dep <= existing_arr or new_arr >= existing_dep):
            last_constraint_error = "Time overlap"
            print(last_constraint_error)
            return False

        # turnaround check
        if new_arr >= existing_dep and (new_arr - existing_dep) < tat:
            last_constraint_error = "Turnaround time not satisfied"
            print(last_constraint_error)
            return False

    return True

# ---------------- CREW ----------------
def check_crew_constraints(crew_list, crew_id, required_aircraft):
    global last_constraint_error
    last_constraint_error = None

    for c in crew_list:

        if c.crew_id == crew_id:

            if c.status != "Available":
                last_constraint_error = "Crew not available"
                print(last_constraint_error)
                return False

            if c.aircraft_type != required_aircraft:
                last_constraint_error = "Not certified"
                print(last_constraint_error)
                return False

            if int(c.duty_hours) > 8:
                last_constraint_error = "Duty exceeded"
                print(last_constraint_error)
                return False

            if int(c.rest_hours) < 8:
                last_constraint_error = "No rest"
                print(last_constraint_error)
                return False

            return True

    last_constraint_error = "Crew not found"
    print(last_constraint_error)
    return False


# ---------------- GATE ----------------
def check_gate_constraints(gate, aircraft_size, flight_type):
    global last_constraint_error
    last_constraint_error = None

    if gate.availability != "Free":
        last_constraint_error = "Gate not available"
        print(last_constraint_error)
        return False

    if gate.max_aircraft_size != aircraft_size:
        last_constraint_error = "Gate size incompatible"
        print(last_constraint_error)
        return False

    if flight_type == "International" and gate.gate_type != "International":
        last_constraint_error = "Gate not suitable for international flights"
        print(last_constraint_error)
        return False

    return True

# ---------------- RUNWAY ----------------
def check_runway_constraints(runway_list, runway_id):
    global last_constraint_error
    last_constraint_error = None

    for r in runway_list:

        if r.runway_id == runway_id:

            if r.availability != "Free":
                last_constraint_error = "Runway occupied"
                print(last_constraint_error)
                return False

            if r.maintenance_window == "Yes":
                last_constraint_error = "Runway under maintenance"
                print(last_constraint_error)
                return False

            return True

    last_constraint_error = "Runway not found"
    print(last_constraint_error)
    return False


# ---------------- RESOURCE ----------------
def check_resource_constraints(resource_list, res_id):
    global last_constraint_error
    last_constraint_error = None

    for r in resource_list:

        if r.res_id == res_id:

            if r.status != "Available":
                last_constraint_error = "Resource in use"
                print(last_constraint_error)
                return False

            return True

    last_constraint_error = "Resource not found"
    print(last_constraint_error)
    return False


# ---------------- DUPLICATE / MODULE-LEVEL CHECKS ----------------
def check_duplicate_aircraft(aircraft_list, aircraft_id):
    global last_constraint_error
    last_constraint_error = None
    if any(a.aircraft_id == aircraft_id for a in aircraft_list):
        last_constraint_error = "Duplicate Aircraft ID"
        print(last_constraint_error)
        return False
    return True


def check_duplicate_crew(crew_list, crew_id):
    global last_constraint_error
    last_constraint_error = None
    if any(c.crew_id == crew_id for c in crew_list):
        last_constraint_error = "Duplicate Crew ID"
        print(last_constraint_error)
        return False
    return True


def check_duplicate_gate(gate_list, gate_id):
    global last_constraint_error
    last_constraint_error = None
    if any(g.gate_id == gate_id for g in gate_list):
        last_constraint_error = "Duplicate Gate ID"
        print(last_constraint_error)
        return False
    return True


def check_duplicate_counter(counter_list, counter_id):
    global last_constraint_error
    last_constraint_error = None
    if any(c.counter_id == counter_id for c in counter_list):
        last_constraint_error = "Duplicate Counter ID not allowed"
        print(last_constraint_error)
        return False
    return True


def check_duplicate_resource(resource_list, res_id):
    global last_constraint_error
    last_constraint_error = None
    if any(r.res_id == res_id for r in resource_list):
        last_constraint_error = "Duplicate Resource ID not allowed"
        print(last_constraint_error)
        return False
    return True


def check_duplicate_runway(runway_list, runway_id):
    global last_constraint_error
    last_constraint_error = None
    if any(r.runway_id == runway_id for r in runway_list):
        last_constraint_error = "Duplicate runway"
        print(last_constraint_error)
        return False
    return True


def check_runway_maintenance_consistency(maintenance_window, maintenance_from, maintenance_to):
    if maintenance_window == "No" and (maintenance_from != "NA" or maintenance_to != "NA"):
        print("Invalid maintenance data")
        return False

    if maintenance_window == "Yes" and (maintenance_from == "NA" or maintenance_to == "NA"):
        print("Missing maintenance time")
        return False

    return True