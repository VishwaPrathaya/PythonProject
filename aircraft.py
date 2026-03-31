from validation import validate_aircraft
from constraint_checking import check_aircraft_constraints


class Aircraft:

    def __init__(self, aircraft_id, flight_no, airline, atype,
                 seating, maintenance, location):

        self.aircraft_id = aircraft_id
        self.flight_no = flight_no
        self.airline = airline
        self.atype = atype
        self.seating = seating
        self.maintenance = maintenance
        self.location = location


def load_aircraft():
    lst = []
    try:
        with open("aircraft.txt") as f:
            for line in f:
                data = line.strip().split(",")
                if len(data) == 7:
                    lst.append(Aircraft(*data))
    except:
        pass
    return lst


def writeData():

    n = int(input("Aircraft count: "))

    with open("aircraft.txt", "a") as f:

        for _ in range(n):

            aid = input("ID: ")
            fno = input("Flight: ")
            airline = input("Airline: ")
            atype = input("Type: ")
            seating = input("Seating: ")

            if not validate_aircraft(aid, fno, atype):
                continue

            maintenance = input("Maintenance (Yes/No): ")
            location = input("Location: ")

            if not check_aircraft_constraints(load_aircraft(), aid, maintenance, location):
                continue

            f.write(",".join([aid, fno, airline, atype, seating, maintenance, location]) + "\n")