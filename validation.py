# Validation Module

# -------------------- FLIGHT --------------------

def validate_flight(flight_id, arrival, departure):

    if flight_id.strip() == "":
        print("Invalid Flight ID")
        return False

    # REMOVE SPACES
    arrival = arrival.strip()
    departure = departure.strip()

    if not arrival.isdigit() or not departure.isdigit():
        print("Arrival/Departure must be numbers")
        return False

    if int(arrival) >= int(departure):
        print("Arrival time must be less than departure time")
        return False

    return True


# -------------------- AIRCRAFT --------------------

def validate_aircraft(aircraft_id, flight_no, aircraft_type):

    if aircraft_id.strip() == "" or flight_no.strip() == "":
        print("Aircraft ID and Flight No cannot be empty")
        return False

    if aircraft_type not in ["Wide", "Narrow"]:
        print("Aircraft type must be Wide or Narrow")
        return False

    return True


# -------------------- CREW --------------------

def validate_crew(crew_id, name, role):

    if crew_id.strip() == "" or name.strip() == "":
        print("Crew ID and Name cannot be empty")
        return False

    if role not in ["Pilot", "Co-Pilot", "Cabin Crew"]:
        print("Invalid role")
        return False

    return True


# -------------------- PASSENGER --------------------

def validate_passenger(passenger_id, name, flight_no, seat_no, ticket_class):

    if passenger_id.strip() == "" or name.strip() == "":
        print("Passenger ID and Name cannot be empty")
        return False

    if flight_no.strip() == "":
        print("Flight number cannot be empty")
        return False

    if seat_no.strip() == "":
        print("Seat number cannot be empty")
        return False

    if ticket_class not in ["Economy", "Business", "First"]:
        print("Invalid ticket class")
        return False

    return True


# -------------------- GATE --------------------

def validate_gate(gate_id, gate_type, max_aircraft_size, availability):

    if gate_id.strip() == "":
        print("Gate ID cannot be empty")
        return False

    if gate_type not in ["Domestic", "International"]:
        print("Invalid gate type")
        return False

    if max_aircraft_size not in ["Wide", "Narrow"]:
        print("Invalid aircraft size")
        return False

    if availability not in ["Free", "Occupied"]:
        print("Invalid availability")
        return False

    return True


# -------------------- RUNWAY --------------------

def validate_runway(length, availability, usage, maintenance_window):

    if not length.isdigit():
        print("Runway length must be numeric")
        return False

    if availability not in ["Free", "Occupied"]:
        print("Invalid availability")
        return False

    if usage not in ["Takeoff", "Landing", "Both"]:
        print("Invalid usage type")
        return False

    if maintenance_window not in ["Yes", "No"]:
        print("Invalid maintenance status")
        return False

    return True


# -------------------- GROUND RESOURCE --------------------

def validate_resource(res_id, res_type, status):

    if res_id.strip() == "" or res_type.strip() == "":
        print("Resource ID/Type cannot be empty")
        return False

    if status not in ["Available", "In Use"]:
        print("Status must be Available or In Use")
        return False

    return True


# -------------------- DISRUPTION --------------------

def validate_disruption(disruption_id, flight_no, dtype, status):

    if disruption_id.strip() == "" or flight_no.strip() == "":
        print("Invalid disruption details")
        return False

    if dtype not in ["Delay", "Technical", "Weather"]:
        print("Invalid disruption type")
        return False

    if status not in ["Resolved", "Pending"]:
        print("Invalid status")
        return False

    return True