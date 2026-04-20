# Class Disruption to store disruption details

from validation import validate_disruption
from constraint_checking import check_disruption_constraints   # ✅ ADDED


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


# Load data from disruption.txt
def load_disruptions():

    disruption_list = []

    try:
        with open("disruption.txt", "r") as f:
            for line in f:
                data = line.strip().split(",")

                if len(data) != 5:
                    print("Invalid disruption data:", line)
                    continue

                d = Disruption(*data)
                disruption_list.append(d)

    except FileNotFoundError:
        print("disruption.txt not found. It will be created when data is added.")

    return disruption_list


# Display disruptions
def display_disruptions():

    disruption_list = load_disruptions()

    if len(disruption_list) == 0:
        print("\nNo disruption data available.")
        return

    print("\n--- Disruption Details ---")

    for d in disruption_list:
        d.display()



# Write data to file
def writeData():

    print("Airport Operations Management System - Disruption Module")

    n = int(input("Enter number of disruptions to add: "))

    with open("disruption.txt", "a") as file:

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

            # 🔥 FIX: TRIGGER INSIDE LOOP
            if disruption_type == "Cancellation":
                print("⚠️ Trigger: Release aircraft, crew, gate, runway")

                from allocation_engine import handle_cancellation
                handle_cancellation(flight_no)

            elif disruption_type == "Delay":
                print("⚠️ Trigger: Reschedule flight")

                from allocation_engine import handle_delay
                handle_delay(flight_no)

            elif disruption_type in ["Technical", "Weather"]:
                print("⚠️ Trigger: Re-optimization required")

                from optimization import optimized_allocation_flow
                optimized_allocation_flow()

    print("\nDisruption details added successfully!")
    display_disruptions()