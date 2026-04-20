
import flights
import gates
import passenger
import runways
import crew
import ground_resources
import disruption_details
import optimization
import aircraft


def main():

    while True:

        print("\n===== AIRPORT OPERATIONS MANAGEMENT SYSTEM =====")
        print("1. Flight Module")
        print("2. Gate Module")
        print("3. Passenger Module")
        print("4. Runway Module")
        print("5. Crew Module")
        print("6. Aircraft Module")
        print("7. Ground Resources Module")
        print("8. Disruption Module")
        print("9. Display All Data")
        print("10. Exit")

        try:
            ch = int(input("\nEnter your choice: "))
        except:
            print("Invalid input. Enter a number.")
            continue

        # -------- FLIGHT (ALREADY AUTO HANDLED INSIDE) --------
        if ch == 1:
            flights.writeData()
            

        # -------- GATE --------
        elif ch == 2:
            gates.writeData()
            gates.display_gates()
            optimization.optimized_allocation_flow()

        # -------- PASSENGER --------
        elif ch == 3:
            passenger.writeData()
            passenger.display_passengers()
            optimization.optimized_allocation_flow()

        # -------- RUNWAY --------
        elif ch == 4:
            runways.writeData()
            runways.display_runways()
            optimization.optimized_allocation_flow()

        # -------- CREW --------
        elif ch == 5:
            crew.writeData()
            crew.display_crew()
            optimization.optimized_allocation_flow()

        # -------- AIRCRAFT --------
        elif ch == 6:
            aircraft.writeData()
            aircraft.display_aircraft()
            optimization.optimized_allocation_flow()

        # -------- GROUND RESOURCES --------
        elif ch == 7:
            ground_resources.writeData()
            ground_resources.display_resources()
            optimization.optimized_allocation_flow()

        # -------- DISRUPTION --------
        elif ch == 8:
            disruption_details.writeData()
            disruption_details.display_disruptions()
            optimization.optimized_allocation_flow()

        # -------- DISPLAY ALL --------
        elif ch == 9:
            print("\n========== ALL DATA ==========")

            flights.display_flights()
            gates.display_gates()
            passenger.display_passengers()
            runways.display_runways()
            crew.display_crew()
            aircraft.display_aircraft()
            ground_resources.display_resources()
            disruption_details.display_disruptions()

        # -------- EXIT --------
        elif ch == 10:
            print("Exiting system...")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()