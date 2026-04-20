from validation import validate_crew
from constraint_checking import check_crew_constraints


class Crew:

    def __init__(self, cid, name, role, fno, shift, atype, status, duty_hours, rest_hours):

        self.crew_id = cid
        self.name = name
        self.role = role
        self.flight_no = fno
        self.shift = shift
        self.aircraft_type = atype
        self.status = status
        self.duty_hours = duty_hours
        self.rest_hours = rest_hours


def load_crew():
    lst = []
    try:
        with open("crew.txt") as f:
            for line in f:
                data = line.strip().split(",")
                if len(data) == 9:
                    lst.append(Crew(*data))
    except:
        pass
    return lst

def display_crew():
    records = load_crew()

    if not records:
        print("\nNo crew data available.")
        return

    for i in records:
        print("\n===== CREW DETAILS =====")
        print("Crew ID        :", i.crew_id)
        print("Name           :", i.name)
        print("Role           :", i.role)
        print("Flight No      :", i.flight_no)
        print("Shift          :", i.shift)
        print("Aircraft Type  :", i.aircraft_type)
        print("Status         :", i.status)
        print("-----------------------------")

def writeData():

    n = int(input("Crew count: "))
    records = load_crew()   # optional for duplicate check

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

            duty = input("Duty Hours: ")
            rest = input("Rest Hours: ")

            # 🔹 simple validation only
            if not duty.isdigit() or not rest.isdigit():
                print("Duty/Rest must be numbers")
                continue

            # optional duplicate check
            if any(c.crew_id == cid for c in records):
                print("Duplicate Crew ID")
                continue

            f.write(",".join([
                cid, name, role, fno, shift,
                atype, status, duty, rest
            ]) + "\n")

            records.append(Crew(
                cid, name, role, fno, shift,
                atype, status, duty, rest
            ))