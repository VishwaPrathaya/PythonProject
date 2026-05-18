# Constraint Checking Module

# -------------------- FLIGHT --------------------
def validate_flight_constraints(flight_list, flight_no, arrival, departure):

    # duplicate safety (extra layer)
    for f in flight_list:
        if f.fno == flight_no:
            print("Flight already exists")
            return False

    if arrival >= departure:
        print("Invalid schedule")
        return False

    return True


# -------------------- PASSENGER --------------------
def check_passenger_constraints(passenger_list, flight_no, seat_no, capacity):

    count = 0

    for p in passenger_list:

        if p.flight_no == flight_no:
            count += 1

            if p.seat_no == seat_no:
                print("Seat already booked")
                return False

    if count >= capacity:
        print("Flight full")
        return False

    return True


# -------------------- DISRUPTION --------------------
def check_disruption_constraints(dtype, status):

    if dtype not in ["Delay", "Technical", "Weather"]:
        print("Invalid type")
        return False

    if status not in ["Resolved", "Pending"]:
        print("Invalid status")
        return False

    return True

# ---------------- AIRCRAFT ----------------
def check_aircraft_constraints(aircraft_list, flight_list, aircraft_id, new_arr, new_dep):

    aircraft = next((a for a in aircraft_list if a.aircraft_id == aircraft_id), None)

    if not aircraft:
        print("Aircraft not found")
        return False

    if aircraft.maintenance.lower() == "yes":
        print("Aircraft under maintenance")
        return False

    if aircraft.location.lower() != "airport":
        print("Aircraft not at airport")
        return False

    tat = aircraft.turnaround_time

    for f in flight_list:

        if f.aircraft != aircraft_id:
            continue

        existing_arr = int(f.arr)
        existing_dep = int(f.dep)

        # overlap check
        if not (new_dep <= existing_arr or new_arr >= existing_dep):
            print("Time overlap")
            return False

        # turnaround check
        if new_arr >= existing_dep and (new_arr - existing_dep) < tat:
            print("Turnaround time not satisfied")
            return False

    return True

# ---------------- CREW ----------------
def check_crew_constraints(crew_list, crew_id, required_aircraft):

    for c in crew_list:

        if c.crew_id == crew_id:

            if c.status != "Available":
                print("Crew not available")
                return False

            if c.aircraft_type != required_aircraft:
                print("Not certified")
                return False

            if int(c.duty_hours) > 8:
                print("Duty exceeded")
                return False

            if int(c.rest_hours) < 8:
                print("No rest")
                return False

            return True

    print("Crew not found")
    return False


# ---------------- GATE ----------------
def check_gate_constraints(gate, aircraft_size, flight_type):

    if gate.availability != "Free":
        print("Gate not available")
        return False

    if gate.max_aircraft_size != aircraft_size:
        print("Gate size incompatible")
        return False

    if flight_type == "International" and gate.gate_type != "International":
        print("Gate not suitable for international flights")
        return False

    return True

# ---------------- RUNWAY ----------------
def check_runway_constraints(runway_list, runway_id):

    for r in runway_list:

        if r.runway_id == runway_id:

            if r.availability != "Free":
                print("Runway occupied")
                return False

            if r.maintenance_window == "Yes":
                print("Runway under maintenance")
                return False

            return True

    print("Runway not found")
    return False


# ---------------- RESOURCE ----------------
def check_resource_constraints(resource_list, res_id):

    for r in resource_list:

        if r.res_id == res_id:

            if r.status != "Available":
                print("Resource in use")
                return False

            return True

    print("Resource not found")
    return False


# ---------------- DUPLICATE / MODULE-LEVEL CHECKS ----------------
def check_duplicate_aircraft(aircraft_list, aircraft_id):
    if any(a.aircraft_id == aircraft_id for a in aircraft_list):
        print("Duplicate Aircraft ID")
        return False
    return True


def check_duplicate_crew(crew_list, crew_id):
    if any(c.crew_id == crew_id for c in crew_list):
        print("Duplicate Crew ID")
        return False
    return True


def check_duplicate_gate(gate_list, gate_id):
    if any(g.gate_id == gate_id for g in gate_list):
        print("Duplicate Gate ID")
        return False
    return True


def check_duplicate_counter(counter_list, counter_id):
    if any(c.counter_id == counter_id for c in counter_list):
        print("Duplicate Counter ID not allowed")
        return False
    return True


def check_duplicate_resource(resource_list, res_id):
    if any(r.res_id == res_id for r in resource_list):
        print("Duplicate Resource ID not allowed")
        return False
    return True


def check_duplicate_runway(runway_list, runway_id):
    if any(r.runway_id == runway_id for r in runway_list):
        print("Duplicate runway")
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