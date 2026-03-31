# Class Passenger to store passenger details
from validation import validate_passenger   # NEW

class Passenger:

    def __init__(self, passenger_id, name, flight_no, seat_no, ticket_class):
        self.passenger_id = passenger_id
        self.name = name
        self.flight_no = flight_no
        self.seat_no = seat_no
        self.ticket_class = ticket_class

    # Display passenger details
    def display(self):
        print("Passenger ID:", self.passenger_id,
              "| Name:", self.name,
              "| Flight:", self.flight_no,
              "| Seat:", self.seat_no,
              "| Class:", self.ticket_class)


# Load passenger data from file
def load_passengers():

    passengers = []

    try:
        with open("passenger.txt", "r") as f:
            for line in f:

                data = line.strip().split(",")

                if len(data) != 5:
                    print("Invalid passenger data:", line)
                    continue

                p = Passenger(*data)
                passengers.append(p)

    except FileNotFoundError:
        print("passenger.txt not found. File will be created when data is added.")

    return passengers


# Display passenger details
def display_passengers():

    passengers = load_passengers()

    if len(passengers) == 0:
        print("\nNo passenger data available.")
        return

    print("\n--- Passenger Details ---")

    for p in passengers:
        p.display()


# Write passenger data
def writeData():

    print("Airport Operations Management System - Passenger Module")

    n = int(input("Enter number of passengers to add: "))

    with open("passenger.txt", "a") as file:

        for i in range(n):

            print("\nEnter details for Passenger", i + 1)

            passenger_id = input("Passenger ID: ")
            name = input("Passenger Name: ")
            flight_no = input("Flight Number: ")
            seat_no = input("Seat Number: ")
            ticket_class = input("Ticket Class (Economy/Business/First): ")

            # ✅ FIXED VALIDATION CALL
            if not validate_passenger(passenger_id, name, flight_no, seat_no, ticket_class):
                print("Invalid input. Skipping this entry...\n")
                continue

            # Only valid data stored
            p = Passenger(passenger_id, name, flight_no,
                          seat_no, ticket_class)

            file.write(passenger_id + "," +
                       name + "," +
                       flight_no + "," +
                       seat_no + "," +
                       ticket_class + "\n")

    print("\nPassengers added successfully!")
    display_passengers()