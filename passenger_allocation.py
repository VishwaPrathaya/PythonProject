from flights import load_flights
from passenger import load_passengers
from allocation_engine import load_allocations, update_flight_file


def allocate_passengers():

    flights = load_flights()
    passengers = load_passengers()
    allocations = load_allocations()

    for f in flights:

        booked = [p for p in passengers if p.fno == f.fno]

        if booked:
            f.status = "ACTIVE"
        else:
            f.status = "EMPTY"

    for p in passengers:
        alloc = allocations.get(p.fno)
        if alloc and len(alloc) > 6:
            p.counter_id = alloc[6]
        else:
            p.counter_id = p.counter_id if getattr(p, "counter_id", "NA") != "NA" else "NA"

    # - SAVE BACK TO FILE
    update_flight_file(flights)

    with open("passenger.csv", "w") as f:
        for p in passengers:
            f.write(",".join([
                p.pid, p.name, p.fno,
                p.seat, p.ticket_class,
                p.status, p.counter_id
            ]) + "\n")

    print(" Passenger allocation updated")