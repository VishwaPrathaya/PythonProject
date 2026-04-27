from flights import load_flights
from passenger import load_passengers


def allocate_passengers():

    flights = load_flights()
    passengers = load_passengers()

    for f in flights:

        booked = [p for p in passengers if p.fno == f.fno]

        if booked:
            f.status = "ACTIVE"
        else:
            f.status = "EMPTY"

    # 🔹 SAVE BACK TO FILE
    from allocation_engine import update_flight_file
    update_flight_file(flights)

    print("✅ Passenger allocation updated")