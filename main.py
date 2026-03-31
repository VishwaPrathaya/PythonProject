import flights
import gates
import passenger
import runways
import crew
import ground_resources
import disruption_details
import optimization


def main():

    while True:

        print("\n===== AIRPORT OPERATIONS MANAGEMENT SYSTEM =====")
        print("1. Flight Module")
        print("2. Gate Module")
        print("3. Passenger Module")
        print("4. Runway Module")
        print("5. Crew Module")
        print("6. Ground Resources Module")
        print("7. Disruption Module")
        print("8. Display All Data")
        print("9. Run Optimization & Allocation")
        print("10. Exit")

        try:
            ch = int(input("Enter your choice: "))
        except:
            print("Invalid input. Enter a number.")
            continue

        # -------- FLIGHT --------
        if ch == 1:
            flights.writeData()
            flights.display_flights()

        # -------- GATE --------
        elif ch == 2:
            gates.writeData()
            gates.display_gates()

        # -------- PASSENGER --------
        elif ch == 3:
            passenger.writeData()
            passenger.display_passengers()

        # -------- RUNWAY --------
        elif ch == 4:
            runways.writeData()
            runways.display_runways()

        # -------- CREW --------
        elif ch == 5:
            crew.writeData()
            crew.display_crew()

        # -------- GROUND RESOURCES --------
        elif ch == 6:
            ground_resources.writeData()
            ground_resources.display_resources()

        # -------- DISRUPTION --------
        elif ch == 7:
            disruption_details.writeData()
            disruption_details.display_disruptions()

        # -------- DISPLAY ALL --------
        elif ch == 8:
            print("\n========== ALL DATA ==========")

            flights.display_flights()
            gates.display_gates()
            passenger.display_passengers()
            runways.display_runways()
            crew.display_crew()
            ground_resources.display_resources()
            disruption_details.display_disruptions()

        # -------- OPTIMIZATION --------
        elif ch == 9:
            optimization.run_allocation()

        # -------- EXIT --------
        elif ch == 10:
            print("Exiting system...")
            break

        else:
            print("Invalid choice. Try again.")


# Run program
if __name__ == "__main__":
    main()