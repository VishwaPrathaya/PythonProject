# Constraint Checking Module

# -------------------- FLIGHT --------------------
def validate_flight_constraints(flight_list, flight_no, arrival, departure, aircraft):

    for f in flight_list:
        if f.fno == flight_no:
            print("Flight number must be unique")
            return False

    if arrival >= departure:
        print("Arrival time must be less than departure time")
        return False

    if aircraft == "" or aircraft == "NA":
        print("Aircraft must be assigned before departure")
        return False

    return True


# -------------------- GATE --------------------
def check_gate_constraints(gate_list, gate_id, aircraft_size, gate_type):

    for g in gate_list:
        if g.gate_id == gate_id:

            if g.availability != "Free":
                print("Gate is occupied")
                return False

            if g.max_aircraft_size != aircraft_size:
                print("Aircraft size not compatible")
                return False

            if gate_type == "International" and g.gate_type != "International":
                print("International needs international gate")
                return False

            return True

    print("Gate not found")
    return False


# -------------------- RUNWAY --------------------
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


# -------------------- CREW --------------------
def check_crew_constraints(crew_list, crew_id, required_aircraft):

    for c in crew_list:

        if c.crew_id == crew_id:
            print("Crew ID must be unique")
            return False

        if c.aircraft_type != required_aircraft:
            print("Crew not certified")
            return False

        if c.status != "Available":
            print("Crew not available")
            return False

    return True


# -------------------- AIRCRAFT --------------------
def check_aircraft_constraints(aircraft_list, aircraft_id, maintenance_status, location):

    for a in aircraft_list:
        if a.aircraft_id == aircraft_id:
            print("Aircraft ID must be unique")
            return False

    if maintenance_status == "Yes":
        print("Aircraft under maintenance")
        return False

    if location == "" or location == "NA":
        print("Invalid location")
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


# -------------------- RESOURCE --------------------
def check_resource_constraints(resource_list, res_id):

    for r in resource_list:

        if r.res_id == res_id:

            if r.status != "Available":
                print("Resource in use")
                return False

            return True

    print("Resource not found")
    return False


# -------------------- DISRUPTION --------------------
def check_disruption_constraints(dtype, status):

    if dtype not in ["Delay", "Technical", "Weather"]:
        print("Invalid type")
        return False

    if status not in ["Resolved", "Pending"]:
        print("Invalid status")
        return False

    return True