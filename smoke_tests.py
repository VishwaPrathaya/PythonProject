"""
Comprehensive Smoke Tests for all validators and constraint checks
"""
import sys
from io import StringIO
import traceback

# Import all validation and constraint checking modules
import validation
import constraint_checking

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
        self.errors = []

    def test(self, name, func, expected_result=None, should_error=False):
        """Run a test and capture results"""
        print(f"\n{'='*60}")
        print(f"TEST: {name}")
        print('='*60)

        try:
            old_stderr = sys.stderr
            sys.stderr = StringIO()
            result = func()
            stderr_output = sys.stderr.getvalue()
            sys.stderr = old_stderr

            if stderr_output:
                print(f"[ERROR OUTPUT] {stderr_output}")
                self.errors.append(f"{name}: {stderr_output}")

            if should_error:
                print(f"? FAILED - Expected error but got: {result}")
                self.failed += 1
                self.tests.append((name, False, f"Expected error but got {result}"))
            else:
                if expected_result is not None and result != expected_result:
                    print(f"? FAILED - Expected {expected_result}, got {result}")
                    self.failed += 1
                    self.tests.append((name, False, f"Expected {expected_result}, got {result}"))
                else:
                    print(f"? PASSED - Result: {result}")
                    self.passed += 1
                    self.tests.append((name, True, str(result)))
        except Exception as e:
            sys.stderr = old_stderr
            if should_error:
                print(f"? PASSED - Got expected error: {str(e)}")
                self.passed += 1
                self.tests.append((name, True, f"Expected error: {str(e)}"))
                self.errors.append(f"{name}: {str(e)}")
            else:
                print(f"? FAILED - Unexpected error: {str(e)}")
                traceback.print_exc()
                self.failed += 1
                self.tests.append((name, False, f"Unexpected error: {str(e)}"))

    def summary(self):
        """Print test summary"""
        print("\n\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Total: {self.passed + self.failed}")

        if self.errors:
            print(f"\n{'='*60}")
            print("ALL ERROR MESSAGES CAPTURED:")
            print('='*60)
            for error in self.errors:
                print(f"  � {error}")


class DummyFlight:
    def __init__(self, fno, capacity):
        self.fno = fno
        self.capacity = capacity


class DummyExistingFlight:
    def __init__(self, fno):
        self.fno = fno


class DummyAircraft:
    def __init__(self, aircraft_id, maintenance, location, turnaround_time):
        self.aircraft_id = aircraft_id
        self.maintenance = maintenance
        self.location = location
        self.turnaround_time = turnaround_time


class DummyFlightConstraint:
    def __init__(self, fno, aircraft, arr, dep):
        self.fno = fno
        self.aircraft = aircraft
        self.arr = arr
        self.dep = dep


class DummyCrewConstraint:
    def __init__(self, crew_id, status, aircraft_type, duty_hours, rest_hours):
        self.crew_id = crew_id
        self.status = status
        self.aircraft_type = aircraft_type
        self.duty_hours = duty_hours
        self.rest_hours = rest_hours


class DummyGate:
    def __init__(self, availability, max_aircraft_size, gate_type, gate_id="G1"):
        self.gate_id = gate_id
        self.availability = availability
        self.max_aircraft_size = max_aircraft_size
        self.gate_type = gate_type


class DummyRunway:
    def __init__(self, runway_id, availability, maintenance_window):
        self.runway_id = runway_id
        self.availability = availability
        self.maintenance_window = maintenance_window


class DummyResource:
    def __init__(self, res_id, status):
        self.res_id = res_id
        self.status = status


class DummyPassengerConstraint:
    def __init__(self, flight_no, seat_no):
        self.flight_no = flight_no
        self.seat_no = seat_no


class TestPassenger:
    def __init__(self, pid, fno, seat):
        self.pid = pid
        self.fno = fno
        self.seat = seat


results = TestResults()

print("AIRCRAFT VALIDATORS")
print("="*60)

results.test(
    "Aircraft type - Valid (Wide)",
    lambda: validation.validate_aircraft("A001", "Wide"),
    expected_result=True
)

results.test(
    "Aircraft type - Invalid type",
    lambda: validation.validate_aircraft("A002", "Helicopter"),
    expected_result=False
)

results.test(
    "Aircraft fields - Valid",
    lambda: validation.validate_aircraft_fields("Narrow", "Yes", 30),
    expected_result=True
)

results.test(
    "Aircraft fields - Invalid maintenance",
    lambda: validation.validate_aircraft_fields("Wide", "Unknown", 30),
    expected_result=False
)

results.test(
    "Aircraft fields - Invalid turnaround time",
    lambda: validation.validate_aircraft_fields("Wide", "No", "thirty"),
    expected_result=False
)

print("\n\nTICKET CLASS VALIDATOR")
print("="*60)

results.test(
    "Ticket class - Valid (Economy)",
    lambda: validation.validate_ticket_class("Economy"),
    expected_result=True
)

results.test(
    "Ticket class - Valid (Business)",
    lambda: validation.validate_ticket_class("Business"),
    expected_result=True
)

results.test(
    "Ticket class - Valid (First)",
    lambda: validation.validate_ticket_class("First"),
    expected_result=True
)

results.test(
    "Ticket class - Invalid",
    lambda: validation.validate_ticket_class("Premium"),
    expected_result=False
)

print("\n\nPASSENGER STATUS VALIDATOR")
print("="*60)

results.test(
    "Passenger status - Valid (Booked)",
    lambda: validation.validate_passenger_status("Booked"),
    expected_result=True
)

results.test(
    "Passenger status - Valid (Checked-In)",
    lambda: validation.validate_passenger_status("Checked-In"),
    expected_result=True
)

results.test(
    "Passenger status - Valid (Boarded)",
    lambda: validation.validate_passenger_status("Boarded"),
    expected_result=True
)

results.test(
    "Passenger status - Invalid",
    lambda: validation.validate_passenger_status("Cancelled"),
    expected_result=False
)

print("\n\nDISRUPTION VALIDATORS")
print("="*60)

results.test(
    "Disruption type - Valid (Weather)",
    lambda: validation.validate_disruption_type("Weather"),
    expected_result=True
)

results.test(
    "Disruption type - Valid (Technical)",
    lambda: validation.validate_disruption_type("Technical"),
    expected_result=True
)

results.test(
    "Disruption type - Invalid",
    lambda: validation.validate_disruption_type("Unknown"),
    expected_result=False
)

results.test(
    "Disruption status - Valid (Pending)",
    lambda: validation.validate_disruption_status("Pending"),
    expected_result=True
)

results.test(
    "Disruption status - Valid (Resolved)",
    lambda: validation.validate_disruption_status("Resolved"),
    expected_result=True
)

results.test(
    "Disruption status - Invalid",
    lambda: validation.validate_disruption_status("Active"),
    expected_result=False
)

results.test(
    "Disruption validation - Valid",
    lambda: validation.validate_disruption("D001", "FL100", "Weather", "Pending"),
    expected_result=True
)

results.test(
    "Disruption validation - Invalid type",
    lambda: validation.validate_disruption("D002", "FL100", "Strike", "Pending"),
    expected_result=False
)

results.test(
    "Disruption priority - Valid (Low)",
    lambda: validation.validate_priority("Low"),
    expected_result=True
)

results.test(
    "Disruption priority - Valid (High)",
    lambda: validation.validate_priority("High"),
    expected_result=True
)

results.test(
    "Disruption priority - Invalid",
    lambda: validation.validate_priority("Urgent"),
    expected_result=False
)

print("\n\nTIME RANGE VALIDATOR")
print("="*60)

results.test(
    "Time range - Valid numeric values",
    lambda: validation.validate_time_range("0800", "1000"),
    expected_result=True
)

results.test(
    "Time range - Invalid non-numeric start",
    lambda: validation.validate_time_range("08:00", "1000"),
    expected_result=False
)

print("\n\nNUMERIC VALIDATORS")
print("="*60)

results.test(
    "Numeric - Valid positive (42)",
    lambda: validation.validate_numeric(42, "Invalid number"),
    expected_result=True
)

results.test(
    "Numeric - Valid zero (0)",
    lambda: validation.validate_numeric(0, "Invalid number"),
    expected_result=True
)

results.test(
    "Numeric - Invalid negative",
    lambda: validation.validate_numeric(-10, "Invalid number"),
    expected_result=False
)

results.test(
    "Numeric - Invalid string",
    lambda: validation.validate_numeric("not a number", "Invalid number"),
    expected_result=False
)

print("\n\nFLIGHT VALIDATION")
print("="*60)

results.test(
    "Flight validation - Valid",
    lambda: validation.validate_flight("FL101", "0800", "1000", "Domestic", "2026-05-18", [DummyExistingFlight("FL100")]),
    expected_result=True
)

results.test(
    "Flight validation - Invalid duplicate",
    lambda: validation.validate_flight("FL100", "0800", "1000", "Domestic", "2026-05-18", [DummyExistingFlight("FL100")]),
    expected_result=False
)

results.test(
    "Flight validation - Invalid times",
    lambda: validation.validate_flight("FL102", "1200", "1000", "Domestic", "2026-05-18", []),
    expected_result=False
)

print("\n\nPASSENGER BOOKING VALIDATION")
print("="*60)

existing_passengers = [
    TestPassenger("P001", "FL100", "1A"),
    TestPassenger("P002", "FL100", "1B")
]

results.test(
    "Passenger booking - Valid",
    lambda: validation.validate_passenger_booking(
        "P003",
        "Alice",
        DummyFlight("FL100", 5),
        "1C",
        existing_passengers,
        lambda fno: sum(1 for p in existing_passengers if p.fno == fno)
    ),
    expected_result=True
)

results.test(
    "Passenger booking - Missing name",
    lambda: validation.validate_passenger_booking(
        "P004",
        "",
        DummyFlight("FL100", 5),
        "1D",
        existing_passengers,
        lambda fno: 0
    ),
    expected_result=False
)

results.test(
    "Passenger booking - Seat already taken",
    lambda: validation.validate_passenger_booking(
        "P005",
        "Bob",
        DummyFlight("FL100", 5),
        "1A",
        existing_passengers,
        lambda fno: sum(1 for p in existing_passengers if p.fno == fno)
    ),
    expected_result=False
)

print("\n\nGATE & RUNWAY VALIDATORS")
print("="*60)

results.test(
    "Gate validation - Valid",
    lambda: validation.validate_gate("G1", "Domestic", "Narrow", "Free"),
    expected_result=True
)

results.test(
    "Gate validation - Invalid type",
    lambda: validation.validate_gate("G1", "Cargo", "Narrow", "Free"),
    expected_result=False
)

results.test(
    "Runway validation - Valid",
    lambda: validation.validate_runway("3000", "Free", "Both", "No"),
    expected_result=True
)

results.test(
    "Runway validation - Invalid usage",
    lambda: validation.validate_runway("3000", "Free", "LandingOnly", "No"),
    expected_result=False
)

print("\n\nCREW VALIDATORS")
print("="*60)

results.test(
    "Crew validation - Valid Pilot",
    lambda: validation.validate_crew("C001", "Jane Doe", "Pilot"),
    expected_result=True
)

results.test(
    "Crew validation - Invalid role",
    lambda: validation.validate_crew("C002", "John Doe", "Mechanic"),
    expected_result=False
)

print("\n\nRESOURCE VALIDATOR")
print("="*60)

results.test(
    "Resource validation - Valid",
    lambda: validation.validate_resource("R001", "Tug", "Available"),
    expected_result=True
)

results.test(
    "Resource validation - Invalid status",
    lambda: validation.validate_resource("R002", "Fuel Truck", "Busy"),
    expected_result=False
)

print("\n\nCONSTRAINT CHECK HELPERS")
print("="*60)

results.test(
    "Check duplicate aircraft - No duplicates",
    lambda: constraint_checking.check_duplicate_aircraft([DummyAircraft("A1", "No", "Airport", 30)], "A2"),
    expected_result=True
)

results.test(
    "Check duplicate aircraft - With duplicates",
    lambda: constraint_checking.check_duplicate_aircraft([DummyAircraft("A1", "No", "Airport", 30), DummyAircraft("A1", "No", "Airport", 30)], "A1"),
    expected_result=False
)

results.test(
    "Check duplicate crew - No duplicates",
    lambda: constraint_checking.check_duplicate_crew([DummyCrewConstraint("C1", "Available", "Wide", 5, 10)], "C2"),
    expected_result=True
)

results.test(
    "Check duplicate crew - With duplicates",
    lambda: constraint_checking.check_duplicate_crew([DummyCrewConstraint("C1", "Available", "Wide", 5, 10), DummyCrewConstraint("C1", "Available", "Wide", 5, 10)], "C1"),
    expected_result=False
)

results.test(
    "Check duplicate gate - No duplicates",
    lambda: constraint_checking.check_duplicate_gate([DummyGate("Free", "Narrow", "Domestic", "G2")], "G1"),
    expected_result=True
)

results.test(
    "Check duplicate gate - With duplicates",
    lambda: constraint_checking.check_duplicate_gate([DummyGate("Free", "Narrow", "Domestic", "G1"), DummyGate("Free", "Narrow", "Domestic", "G1")], "G1"),
    expected_result=False
)

results.test(
    "Check duplicate runway - No duplicates",
    lambda: constraint_checking.check_duplicate_runway([DummyRunway("R1", "Free", "No")], "R2"),
    expected_result=True
)

results.test(
    "Check duplicate runway - With duplicates",
    lambda: constraint_checking.check_duplicate_runway([DummyRunway("R1", "Free", "No"), DummyRunway("R1", "Free", "No")], "R1"),
    expected_result=False
)

results.test(
    "Check duplicate resource - No duplicates",
    lambda: constraint_checking.check_duplicate_resource([DummyResource("RES1", "Available")], "RES2"),
    expected_result=True
)

results.test(
    "Check duplicate resource - With duplicates",
    lambda: constraint_checking.check_duplicate_resource([DummyResource("RES1", "Available"), DummyResource("RES1", "Available")], "RES1"),
    expected_result=False
)

results.test(
    "Runway maintenance consistency - Valid no maintenance",
    lambda: constraint_checking.check_runway_maintenance_consistency("No", "NA", "NA"),
    expected_result=True
)

results.test(
    "Runway maintenance consistency - Valid with maintenance",
    lambda: constraint_checking.check_runway_maintenance_consistency("Yes", "0900", "1100"),
    expected_result=True
)

results.test(
    "Runway maintenance consistency - Invalid missing times",
    lambda: constraint_checking.check_runway_maintenance_consistency("Yes", "NA", "1100"),
    expected_result=False
)

results.test(
    "Check gate constraints - Valid international",
    lambda: constraint_checking.check_gate_constraints(DummyGate("Free", "Wide", "International"), "Wide", "International"),
    expected_result=True
)

results.test(
    "Check gate constraints - Invalid unavailable",
    lambda: constraint_checking.check_gate_constraints(DummyGate("Occupied", "Wide", "International"), "Wide", "International"),
    expected_result=False
)

results.test(
    "Check gate constraints - Invalid size mismatch",
    lambda: constraint_checking.check_gate_constraints(DummyGate("Free", "Narrow", "Domestic"), "Wide", "International"),
    expected_result=False
)

results.test(
    "Check runway constraints - Valid",
    lambda: constraint_checking.check_runway_constraints([DummyRunway("R1", "Free", "No")], "R1"),
    expected_result=True
)

results.test(
    "Check runway constraints - Invalid occupied",
    lambda: constraint_checking.check_runway_constraints([DummyRunway("R1", "Occupied", "No")], "R1"),
    expected_result=False
)

results.test(
    "Check runway constraints - Invalid under maintenance",
    lambda: constraint_checking.check_runway_constraints([DummyRunway("R1", "Free", "Yes")], "R1"),
    expected_result=False
)

results.test(
    "Check crew constraints - Valid",
    lambda: constraint_checking.check_crew_constraints([DummyCrewConstraint("C1", "Available", "Wide", 5, 10)], "C1", "Wide"),
    expected_result=True
)

results.test(
    "Check crew constraints - Invalid not available",
    lambda: constraint_checking.check_crew_constraints([DummyCrewConstraint("C1", "Unavailable", "Wide", 5, 10)], "C1", "Wide"),
    expected_result=False
)

results.test(
    "Check crew constraints - Invalid duty exceeded",
    lambda: constraint_checking.check_crew_constraints([DummyCrewConstraint("C1", "Available", "Wide", 9, 10)], "C1", "Wide"),
    expected_result=False
)

results.test(
    "Check crew constraints - Invalid no rest",
    lambda: constraint_checking.check_crew_constraints([DummyCrewConstraint("C1", "Available", "Wide", 5, 7)], "C1", "Wide"),
    expected_result=False
)

results.test(
    "Check aircraft constraints - Valid",
    lambda: constraint_checking.check_aircraft_constraints(
        [DummyAircraft("AC1", "No", "Airport", 30)],
        [DummyFlightConstraint("FL1", "AC1", 1200, 1300)],
        "AC1",
        1400,
        1500
    ),
    expected_result=True
)

results.test(
    "Check aircraft constraints - Invalid maintenance",
    lambda: constraint_checking.check_aircraft_constraints(
        [DummyAircraft("AC1", "Yes", "Airport", 30)],
        [],
        "AC1",
        1400,
        1500
    ),
    expected_result=False
)

results.test(
    "Check aircraft constraints - Invalid not at airport",
    lambda: constraint_checking.check_aircraft_constraints(
        [DummyAircraft("AC1", "No", "Remote", 30)],
        [],
        "AC1",
        1400,
        1500
    ),
    expected_result=False
)

results.test(
    "Check aircraft constraints - Invalid overlap",
    lambda: constraint_checking.check_aircraft_constraints(
        [DummyAircraft("AC1", "No", "Airport", 30)],
        [DummyFlightConstraint("FL2", "AC1", 1300, 1500)],
        "AC1",
        1400,
        1600
    ),
    expected_result=False
)

results.test(
    "Check passenger constraints - Valid",
    lambda: constraint_checking.check_passenger_constraints([DummyPassengerConstraint("FL100", "2A")], "FL200", "1B", 2),
    expected_result=True
)

results.test(
    "Check passenger constraints - Invalid seat already booked",
    lambda: constraint_checking.check_passenger_constraints([DummyPassengerConstraint("FL100", "2A")], "FL100", "2A", 2),
    expected_result=False
)

results.test(
    "Check passenger constraints - Invalid flight full",
    lambda: constraint_checking.check_passenger_constraints([DummyPassengerConstraint("FL100", "1A"), DummyPassengerConstraint("FL100", "1B")], "FL100", "2C", 2),
    expected_result=False
)

results.test(
    "Validate flight constraints - Valid",
    lambda: constraint_checking.validate_flight_constraints([DummyExistingFlight("FL100")], "FL200", 1000, 1100),
    expected_result=True
)

results.test(
    "Validate flight constraints - Duplicate flight",
    lambda: constraint_checking.validate_flight_constraints([DummyExistingFlight("FL200")], "FL200", 1000, 1100),
    expected_result=False
)

results.test(
    "Validate flight constraints - Invalid schedule",
    lambda: constraint_checking.validate_flight_constraints([], "FL300", 1100, 1000),
    expected_result=False
)

print("\n\nSUMMARY")
print("="*60)
results.summary()

sys.exit(0 if results.failed == 0 else 1)
