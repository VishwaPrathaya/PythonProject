from validation import validate_crew
from constraint_checking import check_crew_constraints


class Crew:

    def __init__(self, cid, name, role, fno, shift, atype, status):

        self.crew_id = cid
        self.name = name
        self.role = role
        self.flight_no = fno
        self.shift = shift
        self.aircraft_type = atype
        self.status = status


def load_crew():
    lst = []
    try:
        with open("crew.txt") as f:
            for line in f:
                data = line.strip().split(",")
                if len(data) == 7:
                    lst.append(Crew(*data))
    except:
        pass
    return lst


def writeData():

    n = int(input("Crew count: "))

    with open("crew.txt", "a") as f:

        for _ in range(n):

            cid = input("ID: ")
            name = input("Name: ")
            role = input("Role: ")
            fno = input("Flight: ")
            shift = input("Shift: ")

            if not validate_crew(cid, name, role):
                continue

            atype = input("Aircraft Type: ")
            status = input("Status: ")

            if not check_crew_constraints(load_crew(), cid, atype):
                continue

            f.write(",".join([cid, name, role, fno, shift, atype, status]) + "\n")