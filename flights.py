from validation import validate_flight
from constraint_checking import validate_flight_constraints


class Flight:

    def __init__(self, fno, arr, dep, aircraft):
        self.fno = fno
        self.arr = arr
        self.dep = dep
        self.aircraft = aircraft


def load_flights():
    lst = []
    try:
        with open("flights.txt") as f:
            for line in f:
                data = line.strip().split(",")
                if len(data) == 4:
                    lst.append(Flight(*data))
    except:
        pass
    return lst


def writeData():

    n = int(input("Flights count: "))

    with open("flights.txt", "a") as f:

        for _ in range(n):

            fno = input("Flight No: ")
            arr = input("Arrival: ")
            dep = input("Departure: ")
            aircraft = input("Aircraft ID: ")

            if not validate_flight(fno, arr, dep):
                continue

            if not validate_flight_constraints(load_flights(), fno, int(arr), int(dep), aircraft):
                continue

            f.write(",".join([fno, arr, dep, aircraft]) + "\n")