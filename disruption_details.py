# Class Disruption to store disruption details

from validation import validate_disruption, validate_disruption_type, validate_disruption_status, validate_priority


class Disruption:

    def __init__(self, disruption_id, flight_no, disruption_type, status, priority):
        self.disruption_id = disruption_id
        self.flight_no = flight_no
        self.disruption_type = disruption_type
        self.status = status
        self.priority = priority

    # Display method
    def display(self):
        print("Disruption ID:", self.disruption_id,
              "| Flight:", self.flight_no,
              "| Type:", self.disruption_type,
              "| Status:", self.status)


# ---------------- LOAD ----------------
def load_disruptions():

    disruption_list = []

    try:
        with open("disruption.csv", "r") as f:
            for line in f:
                data = line.strip().split(",")

                if len(data) != 5:
                    print("Invalid disruption data:", line)
                    continue

                disruption_list.append(Disruption(*data))

    except FileNotFoundError:
        pass

    return disruption_list


# ---------------- DISPLAY ----------------
def display_disruptions():

    disruption_list = load_disruptions()

    if not disruption_list:
        print("\nNo disruption data available.")
        return

    print("\n--- Disruption Details ---")

    for d in disruption_list:
        d.display()


# ---------------- REMOVE ----------------
def remove_disruption():

    disruptions = load_disruptions()

    if not disruptions:
        print("No disruptions to remove")
        return

    did = input("Enter Disruption ID to remove: ")

    updated = []
    target = None

    for d in disruptions:
        if d.disruption_id == did:
            target = d
        else:
            updated.append(d)

    if not target:
        print("Disruption not found")
        return

    #  SYSTEM RESPONSE (ONLY IF ACTIVE)
    if target.status == "Pending":
        print(" Active disruption removed → restoring system")

        from allocation_engine import try_schedule_pending_flights
        try_schedule_pending_flights()

    # - SAVE FILE
    with open("disruption.csv", "w") as f:
        for d in updated:
            f.write(",".join([
                d.disruption_id,
                d.flight_no,
                d.disruption_type,
                d.status,
                d.priority
            ]) + "\n")

    print("- Disruption removed successfully")


# ---------------- WRITE ----------------
def writeData():

    print("Airport Operations Management System - Disruption Module")

    n = int(input("Enter number of disruptions to add: "))

    with open("disruption.csv", "a") as file:

        for i in range(n):

            print("\nEnter details for Disruption", i + 1)

            disruption_id = input("Disruption ID: ")
            flight_no = input("Flight Number: ")
            disruption_type = input("Type (Delay/Technical/Weather/Cancellation): ")
            status = input("Status (Resolved/Pending): ")
            priority = input("Priority (High/Medium/Low): ")

            # STEP 1: VALIDATION
            if not validate_disruption(disruption_id, flight_no, disruption_type, status):
                print("Invalid input. Skipping this entry...\n")
                continue

            # CREATE OBJECT
            d = Disruption(disruption_id, flight_no, disruption_type, status, priority)

            # SAVE
            file.write(",".join([
                disruption_id, flight_no,
                disruption_type, status, priority
            ]) + "\n")

            # - TRIGGER (VERY IMPORTANT FOR SYSTEM + VIVA)
            if disruption_type == "Cancellation":
                print("- Trigger: Release aircraft, crew, gate, runway")

                from allocation_engine import handle_cancellation
                handle_cancellation(flight_no)

            elif disruption_type == "Delay":
                print("- Trigger: Reschedule flight")

                from allocation_engine import handle_delay
                handle_delay(flight_no)

            elif disruption_type in ["Technical", "Weather"]:
                print(" Trigger: System re-optimization")

                from optimization import optimized_allocation_flow
                optimized_allocation_flow()

    print("\nDisruption details added successfully!")
    display_disruptions()


# ---------------- UPDATE ----------------
def update_disruption():

    disruptions = load_disruptions()

    if not disruptions:
        print("No disruptions available")
        return

    did = input("Enter Disruption ID to update: ")

    target = next((d for d in disruptions if d.disruption_id == did), None)

    if not target:
        print("Disruption not found")
        return

    print(f"\nCurrent: {target.disruption_id} | {target.flight_no} | {target.disruption_type} | {target.status}")
    print("Leave blank to keep current value\n")

    dtype = input(f"Type [{target.disruption_type}]: ").strip()
    status = input(f"Status [{target.status}]: ").strip()
    priority = input(f"Priority [{target.priority}]: ").strip()

    old_status = target.status

    if dtype:
        if not validate_disruption_type(dtype):
            return
        target.disruption_type = dtype

    if status:
        if not validate_disruption_status(status):
            return
        target.status = status

    if priority:
        if not validate_priority(priority):
            return
        target.priority = priority

    #  SAVE FILE
    with open("disruption.csv", "w") as f:
        for d in disruptions:
            f.write(",".join([
                d.disruption_id,
                d.flight_no,
                d.disruption_type,
                d.status,
                d.priority
            ]) + "\n")

    print(f" Disruption {did} updated successfully")

    # - SYSTEM RESPONSE
    _handle_disruption_update(target, old_status)


# ---------------- SYSTEM HANDLER ----------------
def _handle_disruption_update(disruption, old_status):

    fno = disruption.flight_no

    #  CASE 1: RESOLVED → restore system
    if disruption.status == "Resolved" and old_status != "Resolved":

        print("Reallocation triggered (disruption resolved)")

        from allocation_engine import try_schedule_pending_flights
        try_schedule_pending_flights()

    #  CASE 2: STILL PENDING → apply disruption logic
    elif disruption.status == "Pending":

        if disruption.disruption_type == "Cancellation":

            print("Trigger: Release aircraft, crew, gate, runway")

            from allocation_engine import remove_allocation_for_flight
            remove_allocation_for_flight(fno)

        elif disruption.disruption_type == "Delay":

            print("Trigger: Reschedule flight")

            from allocation_engine import try_schedule_pending_flights
            try_schedule_pending_flights()

        elif disruption.disruption_type in ["Technical", "Weather"]:

            print("Trigger: Re-optimization required")

            from optimization import optimized_allocation_flow
            optimized_allocation_flow()