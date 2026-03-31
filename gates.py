# Class Gate to store gate details

from validation import validate_gate
from constraint_checking import check_gate_constraints  


class Gate:
    def __init__(self, gate_id, terminal_no, gate_type,
                 max_aircraft_size, availability):

        self.gate_id = gate_id
        self.terminal_no = terminal_no
        self.gate_type = gate_type
        self.max_aircraft_size = max_aircraft_size
        self.availability = availability

    # Display method
    def display(self):
        print("Gate ID:", self.gate_id,
              "| Terminal:", self.terminal_no,
              "| Type:", self.gate_type,
              "| Max Size:", self.max_aircraft_size,
              "| Status:", self.availability)


# Load gate data from gates.txt
def load_gates():
    gates = []

    try:
        with open("gates.txt", "r") as f:
            for line in f:
                data = line.strip().split(",")

                if len(data) != 5:
                    print("Invalid gate data:", line)
                    continue

                gate = Gate(*data)
                gates.append(gate)

    except FileNotFoundError:
        print("gates.txt not found. It will be created when data is added.")

    return gates


# Display gate details
def display_gates():
    gates = load_gates()

    if len(gates) == 0:
        print("\nNo gate data available.")
        return

    print("\n--- Gate Details ---")
    for g in gates:
        g.display()


# Write gate data to file
def writeData():
    print("Airport Operations Management System - Gate Module")

    n = int(input("Enter number of gates to add: "))

    with open("gates.txt", "a") as file:

        for i in range(n):
            print("\nEnter details for Gate", i + 1)

            gate_id = input("Gate ID: ")
            terminal_no = input("Terminal Number: ")
            gate_type = input("Gate Type (Domestic/International): ")
            max_aircraft_size = input("Max Aircraft Size Supported (Wide/Narrow): ")
            availability = input("Availability Status (Free/Occupied): ")

            # STEP 1: VALIDATION
            if not validate_gate(gate_id, gate_type, max_aircraft_size, availability):
                print("Invalid input. Skipping this entry...\n")
                continue

            # STEP 2: CONSTRAINT CHECK
            if not check_gate_constraints(load_gates(), gate_id,
                                          max_aircraft_size, gate_type):
                print("Constraint violation. Skipping this entry...\n")
                continue

            # Only valid + constraint-safe data stored
            g = Gate(gate_id, terminal_no,
                     gate_type, max_aircraft_size,
                     availability)

            file.write(gate_id + "," +
                       terminal_no + "," +
                       gate_type + "," +
                       max_aircraft_size + "," +
                       availability + "\n")

    print("\nGates added successfully!")
    display_gates()