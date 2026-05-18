import flights
import gates
import passenger
import runways
import crew
import ground_resources
import disruption_details
import optimization
import aircraft
import counters
import conflict_resolution


def main():

    while True:

        print("\n===== AIRPORT OPERATIONS MANAGEMENT SYSTEM =====")
        print("1. Flight Module")
        print("2. Gate Module")
        print("3. Counter Module")
        print("4. Passenger Module")
        print("5. Runway Module")
        print("6. Crew Module")
        print("7. Aircraft Module")
        print("8. Ground Resources Module")
        print("9. Disruption Module")
        print("10. Display All Data")
        print("11. Run Cleanup (release expired allocations)")
        print("12. Resolve Conflicts")
        print("13. Exit")

        try:
            ch = int(input("\nEnter your choice: "))
        except:
            print("Invalid input. Enter a number.")
            continue

        # -------- FLIGHT --------
        if ch == 1:
            print("\n--- Flight Module ---")
            print("1. Load Flights")
            print("2. Add Flight")
            print("3. Remove Flight")
            print("4. Update Flight")
            print("5. Display Flights")

            fch = input("Choice: ")

            if fch == "1":
                loaded_flights = flights.load_flights()
                print(f"Loaded {len(loaded_flights)} flights.")
            elif fch == "2":
                flights.writeData()
            elif fch == "3":
                flights.remove_flight()
            elif fch == "4":
                flights.update_flight()
            elif fch == "5":
                flights.display_flights()
            else:
                print("Invalid choice")

        # -------- GATE --------
        elif ch == 2:
            print("\n--- Gate Module ---")
            print("1. Load Gates")
            print("2. Remove Gate")
            print("3. Update Gate")
            print("4. Display Gates")

            gch = input("Choice: ")

            if gch == "1":
                loaded_gates = gates.load_gates()
                print(f"Loaded {len(loaded_gates)} gates.")
            elif gch == "2":
                gates.remove_gate()
            elif gch == "3":
                gates.update_gate()
            elif gch == "4":
                gates.display_gates()
            else:
                print("Invalid choice")

        # -------- COUNTERS --------
        elif ch == 3:
            print("\n--- Counter Module ---")
            print("1. Load Counters")
            print("2. Add Counter")
            print("3. Remove Counter")
            print("4. Update Counter")
            print("5. Display Counters")

            cch = input("Choice: ")

            if cch == "1":
                loaded_counters = counters.load_counters()
                print(f"Loaded {len(loaded_counters)} counters.")
            elif cch == "2":
                counters.add_counter()
            elif cch == "3":
                counters.remove_counter()
            elif cch == "4":
                counters.update_counter()
            elif cch == "5":
                counters.display_counters()
            else:
                print("Invalid choice")

        # -------- PASSENGER --------
        elif ch == 4:
            print("\n--- Passenger Module ---")
            print("1. Load Passengers")
            print("2. Book Flight")
            print("3. Add Passenger")
            print("4. Remove Passenger")
            print("5. Update Passenger")
            print("6. Display Passengers")

            pch = input("Choice: ")

            if pch == "1":
                loaded_passengers = passenger.load_passengers()
                print(f"Loaded {len(loaded_passengers)} passengers.")
            elif pch == "2":
                from passenger_booking import book_flight
                book_flight()
            elif pch == "3":
                passenger.writeData()
            elif pch == "4":
                passenger.remove_passenger()
            elif pch == "5":
                passenger.update_passenger()
            elif pch == "6":
                passenger.display_passengers()
            else:
                print("Invalid choice")

        # -------- RUNWAY --------
        elif ch == 5:
            print("\n--- Runway Module ---")
            print("1. Load Runways")
            print("2. Remove Runway")
            print("3. Update Runway")
            print("4. Display Runways")

            rch = input("Choice: ")

            if rch == "1":
                loaded_runways = runways.load_runways()
                print(f"Loaded {len(loaded_runways)} runways.")
            elif rch == "2":
                runways.remove_runway()
            elif rch == "3":
                runways.update_runway()
            elif rch == "4":
                runways.display_runways()
            else:
                print("Invalid choice")

        # -------- CREW --------
        elif ch == 6:
            print("\n--- Crew Module ---")
            print("1. Load Crew")
            print("2. Add Crew")
            print("3. Remove Crew")
            print("4. Update Crew")
            print("5. Display Crew")

            cch = input("Choice: ")

            if cch == "1":
                loaded_crew = crew.load_crew()
                print(f"Loaded {len(loaded_crew)} crew members.")
            elif cch == "2":
                crew.writeData()
                optimization.optimized_allocation_flow()
            elif cch == "3":
                crew.remove_crew()
            elif cch == "4":
                crew.update_crew()
            elif cch == "5":
                crew.display_crew()
            else:
                print("Invalid choice")

        # -------- AIRCRAFT --------
        elif ch == 7:
            print("\n--- Aircraft Module ---")
            print("1. Load Aircraft")
            print("2. Add Aircraft")
            print("3. Remove Aircraft")
            print("4. Update Aircraft")
            print("5. Display Aircraft")

            ach = input("Choice: ")

            if ach == "1":
                loaded_aircraft = aircraft.load_aircraft()
                print(f"Loaded {len(loaded_aircraft)} aircraft.")
            elif ach == "2":
                aircraft.writeData()
                optimization.optimized_allocation_flow()
            elif ach == "3":
                aircraft.remove_aircraft()
            elif ach == "4":
                aircraft.update_aircraft()
            elif ach == "5":
                aircraft.display_aircraft()
            else:
                print("Invalid choice")

        # -------- GROUND RESOURCES --------
        elif ch == 8:
            print("\n--- Resource Module ---")
            print("1. Load Resources")
            print("2. Add Resource")
            print("3. Remove Resource")
            print("4. Update Resource")
            print("5. Display Resources")

            rch = input("Choice: ")

            if rch == "1":
                loaded_resources = ground_resources.load_resources()
                print(f"Loaded {len(loaded_resources)} resources.")
            elif rch == "2":
                ground_resources.writeData()
                optimization.optimized_allocation_flow()
            elif rch == "3":
                ground_resources.remove_resource()
            elif rch == "4":
                ground_resources.update_resource()
            elif rch == "5":
                ground_resources.display_resources()
            else:
                print("Invalid choice")

        # -------- DISRUPTION --------
        elif ch == 9:
            print("\n--- Disruption Module ---")
            print("1. Load Disruptions")
            print("2. Add Disruption")
            print("3. Remove Disruption")
            print("4. Update Disruption")
            print("5. Display Disruptions")

            dch = input("Choice: ")

            if dch == "1":
                loaded_disruptions = disruption_details.load_disruptions()
                print(f"Loaded {len(loaded_disruptions)} disruptions.")
            elif dch == "2":
                disruption_details.writeData()
                optimization.optimized_allocation_flow()
            elif dch == "3":
                disruption_details.remove_disruption()
            elif dch == "4":
                disruption_details.update_disruption()
            elif dch == "5":
                disruption_details.display_disruptions()
            else:
                print("Invalid choice")

        # -------- DISPLAY ALL --------
        elif ch == 10:
            print("\n========== ALL DATA ==========")

            flights.display_flights()
            gates.display_gates()
            counters.display_counters()
            passenger.display_passengers()
            runways.display_runways()
            crew.display_crew()
            aircraft.display_aircraft()
            ground_resources.display_resources()
            disruption_details.display_disruptions()

        # -------- CLEANUP --------
        elif ch == 11:
            from allocation_engine import release_expired_allocations
            print("Running cleanup: releasing expired allocations...")
            release_expired_allocations()

        # -------- CONFLICT RESOLUTION --------
        elif ch == 12:
            print("Running conflict resolution...")
            conflict_resolution.resolve_conflicts()

        # -------- EXIT --------
        elif ch == 13:
            print("Exiting system...")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()