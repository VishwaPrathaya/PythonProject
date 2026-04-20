from data_loader import load_flights
from passenger import load_passengers


def allocate_passengers():

    flights = load_flights()
    passengers = load_passengers()

    for f in flights:

        booked = [p for p in passengers if p.fno == f.fno]

        if booked:
            f.status = "ACTIVE"

    print("Passenger allocation updated")