# Validation Module

from passenger import load_passengers, seats_used

# -------------------- FLIGHT --------------------
def validate_flight(flight_id, arrival, departure, flight_type, date, existing_flights):

    if flight_id.strip() == "":
        print("Invalid Flight ID")
        return False

    # 🔹 duplicate check
    for f in existing_flights:
        if f.fno == flight_id:
            print("Duplicate Flight ID not allowed")
            return False

    # 🔹 time validation
    if not arrival.isdigit() or not departure.isdigit():
        print("Arrival/Departure must be numbers")
        return False

    if int(arrival) >= int(departure):
        print("Arrival must be < Departure")
        return False

    # 🔹 flight type validation (NEW)
    if flight_type not in ["Domestic", "International"]:
        print("Invalid Flight Type")
        return False

    # 🔹 date validation (basic check)
    if date.strip() == "":
        print("Date cannot be empty")
        return False

    return True
# -------------------- AIRCRAFT --------------------

def validate_aircraft(aircraft_id, atype):

    if aircraft_id.strip() == "":
        print("Aircraft ID cannot be empty")
        return False

    if atype not in ["Wide", "Narrow"]:
        print("Invalid aircraft type")
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



def validate_passenger_booking(pid, name, flight, seat, passengers, seats_used_func):

    # ---------------- EMPTY CHECK ----------------
    if pid.strip() == "" or name.strip() == "":
        print(" Passenger ID and Name cannot be empty")
        return False

    # ---------------- FLIGHT CHECK ----------------
    if flight is None:
        print("- Invalid flight selected")
        return False

    # ---------------- FLIGHT ID CHECK ----------------
    if not hasattr(flight, "fno") or flight.fno.strip() == "":
        print("- Flight data corrupted")
        return False

    # ---------------- SEAT CHECK ----------------
    if seat.strip() == "":
        print("- Seat number cannot be empty")
        return False

    # ---------------- DUPLICATE BOOKING CHECK ----------------
    for p in passengers:
        if p.pid == pid and p.fno == flight.fno:
            print("- Already booked this flight")
            return False

    # ---------------- SEAT ALREADY TAKEN ----------------
    for p in passengers:
        if p.fno == flight.fno and p.seat == seat:
            print("- Seat already taken")
            return False

    # ---------------- CAPACITY CHECK ----------------
    if not hasattr(flight, "capacity"):
        print("- Flight capacity missing")
        return False

    capacity = int(flight.capacity)

    if seats_used_func(flight.fno) >= capacity:
        print("- Flight is full")
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

    if dtype not in ["Delay", "Technical", "Weather", "Cancellation"]:
        print("Invalid disruption type")
        return False

    if status not in ["Resolved", "Pending"]:
        print("Invalid status")
        return False

    return True