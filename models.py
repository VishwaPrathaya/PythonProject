
class Flight:

    def __init__(self, fno, airline, origin, destination,
                 arr, dep, date, aircraft="NA", flight_type="Domestic",capacity="100"):

        self.fno = fno
        self.airline = airline
        self.origin = origin
        self.destination = destination
        self.arr = arr
        self.dep = dep
        self.date = date
        self.aircraft = aircraft
        self.flight_type = flight_type
        self.capacity = int(capacity)