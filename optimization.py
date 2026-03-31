import flights
import gates
import runways
import crew
import ground_resources


# ---------------- GATE ALLOCATION ----------------
def allocate_gate():

    flight_list = flights.load_flights()
    gate_list = gates.load_gates()

    print("\n--- Gate Allocation ---")

    for f in flight_list:

        for g in gate_list:

            if g.availability == "Free":

                print("Flight", f.fno, "-> Gate", g.gate_id)

                g.availability = "Occupied"
                break

        else:
            print("No gate available for Flight", f.fno)


# ---------------- RUNWAY ALLOCATION ----------------
def allocate_runway():

    flight_list = flights.load_flights()
    runway_list = runways.load_runways()

    print("\n--- Runway Allocation ---")

    for f in flight_list:

        for r in runway_list:

            if r.availability == "Free" and r.maintenance_window == "No":

                print("Flight", f.fno, "-> Runway", r.runway_id)

                r.availability = "Occupied"
                break

        else:
            print("No runway available for Flight", f.fno)


# ---------------- CREW ALLOCATION ----------------
def allocate_crew():

    flight_list = flights.load_flights()
    crew_list = crew.load_crew()

    print("\n--- Crew Allocation ---")

    for f in flight_list:

        for c in crew_list:

            if c.status == "Available":

                print("Flight", f.fno, "-> Crew", c.crew_id)

                c.status = "Busy"
                break

        else:
            print("No crew available for Flight", f.fno)


# ---------------- RESOURCE ALLOCATION ----------------
def allocate_resources():

    flight_list = flights.load_flights()
    resource_list = ground_resources.load_resources()

    print("\n--- Resource Allocation ---")

    for f in flight_list:

        for r in resource_list:

            if r.status == "Available":

                print("Flight", f.fno, "-> Resource", r.res_id)

                r.status = "In Use"
                break

        else:
            print("No resource available for Flight", f.fno)


# ---------------- MAIN FUNCTION ----------------
def run_allocation():

    allocate_gate()
    allocate_runway()
    allocate_crew()
    allocate_resources()