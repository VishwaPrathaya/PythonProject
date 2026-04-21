from models import Flight
from aircraft import Aircraft



# ---------------- LOAD ----------------
def load_flights():

    flights = []

    try:
        with open("flights.txt", "r") as f:
            for line in f:
                data = line.strip().split(",")

                if len(data) != 10:
                    continue

                flights.append(Flight(*data))
                

    except FileNotFoundError:
        pass

    return flights

###def load_aircraft():

    lst = []

    try:
        with open("aircraft.txt") as f:
            for line in f:
                data = line.strip().split(",")

                if len(data) != 5:
                    continue

                lst.append(Aircraft(*data))

    except FileNotFoundError:
        pass

    return lst

###def load_passengers():

    lst = []

    try:
        with open("passenger.txt") as f:
            for line in f:
                data = line.strip().split(",")

                if len(data) != 6:
                    continue

                lst.append(Passenger(*data))

    except FileNotFoundError:
        pass

    return lst



###def load_passengers():

    class Passenger:
        def __init__(self, pid, name, fno, seat, pclass="Economy", status="Booked"):
            self.pid = pid
            self.name = name
            self.fno = fno
            self.seat = seat
            self.pclass = pclass
            self.status = status

    lst = []

    try:
        with open("passenger.txt") as f:
            for line in f:
                data = line.strip().split(",")

                if len(data) < 4:
                    continue

                lst.append(Passenger(*data))
    except:
        pass

    return lst