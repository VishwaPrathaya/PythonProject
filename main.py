
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
            print("\n--- Flight Module ---")
            print("1. Add Flight")
            print("2. Remove Flight")
            print("3. Display Flights")

            fch = input("Choice: ")

            if fch == "1":
                flights.writeData()
            elif fch == "2":
                flights.remove_flight()   # ✅ ADD THIS
            elif fch == "3":
                flights.display_flights()
            else:
                print("Invalid choice")
                    

        # -------- GATE --------
        elif ch == 2:
            print("\n--- Gate Module ---")
            print("1. Add Gate")
            print("2. Remove Gate")
            print("3. Display Gates")

            gch = input("Choice: ")

            if gch == "1":
                gates.writeData()
                optimization.optimized_allocation_flow()
            elif gch == "2":
                gates.remove_gate()   # ✅
            elif gch == "3":
                gates.display_gates()
            else:
                print("Invalid choice")

        # -------- PASSENGER --------
        elif ch == 3:
            print("\n--- Passenger Module ---")
            print("1. Book Flight")
            print("2. Add Passenger")
            print("3. Remove Passenger")
            print("4. Display Passengers")

            pch = input("Choice: ")

            if pch == "1":
                from passenger_booking import book_flight
                book_flight()
            elif pch == "2":
                passenger.writeData()
            elif pch == "3":
                passenger.remove_passenger()   # ✅
            elif pch == "4":
                passenger.display_passengers()
            else:
                print("Invalid choice")
        # -------- RUNWAY --------
        elif ch == 4:
            print("\n--- Runway Module ---")
            print("1. Add Runway")
            print("2. Remove Runway")
            print("3. Display Runways")

            rch = input("Choice: ")

            if rch == "1":
                runways.writeData()
                optimization.optimized_allocation_flow()
            elif rch == "2":
                runways.remove_runway()   # ✅
            elif rch == "3":
                runways.display_runways()

        # -------- CREW --------
        elif ch == 5:
            print("\n--- Crew Module ---")
            print("1. Add Crew")
            print("2. Remove Crew")
            print("3. Display Crew")

            cch = input("Choice: ")

            if cch == "1":
                crew.writeData()
                optimization.optimized_allocation_flow()
            elif cch == "2":
                crew.remove_crew()   # ✅
            elif cch == "3":
                crew.display_crew()
        # -------- AIRCRAFT --------
        elif ch == 6:
            print("\n--- Aircraft Module ---")
            print("1. Add Aircraft")
            print("2. Remove Aircraft")
            print("3. Display Aircraft")

            ach = input("Choice: ")

            if ach == "1":
                aircraft.writeData()
                optimization.optimized_allocation_flow()
            elif ach == "2":
                aircraft.remove_aircraft()   # ✅
            elif ach == "3":
                aircraft.display_aircraft()

        # -------- GROUND RESOURCES --------
        elif ch == 7:
            print("\n--- Resource Module ---")
            print("1. Add Resource")
            print("2. Remove Resource")
            print("3. Display Resources")

            rch = input("Choice: ")

            if rch == "1":
                ground_resources.writeData()
                optimization.optimized_allocation_flow()
            elif rch == "2":
                ground_resources.remove_resource()   # ✅
            elif rch == "3":
                ground_resources.display_resources()

        # -------- DISRUPTION --------
        elif ch == 8:
            print("\n--- Disruption Module ---")
            print("1. Add Disruption")
            print("2. Remove Disruption")
            print("3. Display Disruptions")

            dch = input("Choice: ")

            if dch == "1":
                disruption_details.writeData()
                optimization.optimized_allocation_flow()
            elif dch == "2":
                disruption_details.remove_disruption()   # ✅
            elif dch == "3":
                disruption_details.display_disruptions()
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