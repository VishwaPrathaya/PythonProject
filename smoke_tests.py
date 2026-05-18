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
            # Capture stderr for error messages
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
                print(f"  • {error}")

# Initialize test results
results = TestResults()

print("AIRCRAFT VALIDATORS")
print("="*60)

# Aircraft type validation
results.test(
    "Aircraft type - Valid (Boeing 747)",
    lambda: validation.validate_aircraft("type", "Boeing 747"),
    expected_result=True
)

results.test(
    "Aircraft type - Invalid",
    lambda: validation.validate_aircraft("type", "Helicopter"),
    should_error=True
)

# Aircraft maintenance validation
results.test(
    "Aircraft maintenance - Valid (Pending)",
    lambda: validation.validate_aircraft("maintenance_status", "Pending"),
    expected_result=True
)

results.test(
    "Aircraft maintenance - Invalid",
    lambda: validation.validate_aircraft("maintenance_status", "Unknown"),
    should_error=True
)

# Aircraft turnaround time validation
results.test(
    "Aircraft turnaround time - Valid (30)",
    lambda: validation.validate_aircraft("turnaround_time", 30),
    expected_result=True
)

results.test(
    "Aircraft turnaround time - Invalid (negative)",
    lambda: validation.validate_aircraft("turnaround_time", -5),
    should_error=True
)

print("\n\nTICKET CLASS VALIDATOR")
print("="*60)

# Ticket class validation
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
    should_error=True
)

print("\n\nPASSENGER STATUS VALIDATOR")
print("="*60)

# Passenger status validation
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
    should_error=True
)

print("\n\nDISRUPTION VALIDATORS")
print("="*60)

# Disruption type validation
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
    should_error=True
)

# Disruption status validation
results.test(
    "Disruption status - Valid (Active)",
    lambda: validation.validate_disruption_status("Active"),
    expected_result=True
)

results.test(
    "Disruption status - Valid (Resolved)",
    lambda: validation.validate_disruption_status("Resolved"),
    expected_result=True
)

results.test(
    "Disruption status - Invalid",
    lambda: validation.validate_disruption_status("Pending"),
    should_error=True
)

# Priority validation
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
    should_error=True
)

print("\n\nTIME RANGE VALIDATOR")
print("="*60)

# Time range validation
results.test(
    "Time range - Valid (08:00-10:00)",
    lambda: validation.validate_time_range("08:00-10:00"),
    expected_result=True
)

results.test(
    "Time range - Valid (14:30-16:45)",
    lambda: validation.validate_time_range("14:30-16:45"),
    expected_result=True
)

results.test(
    "Time range - Invalid format",
    lambda: validation.validate_time_range("8:00-10:00"),
    should_error=True
)

results.test(
    "Time range - Invalid (end before start)",
    lambda: validation.validate_time_range("10:00-08:00"),
    should_error=True
)

print("\n\nNUMERIC VALIDATORS")
print("="*60)

# Numeric validation (positive)
results.test(
    "Numeric - Valid positive (42)",
    lambda: validation.validate_numeric(42),
    expected_result=True
)

results.test(
    "Numeric - Valid positive (0)",
    lambda: validation.validate_numeric(0),
    expected_result=True
)

results.test(
    "Numeric - Invalid (negative)",
    lambda: validation.validate_numeric(-10),
    should_error=True
)

results.test(
    "Numeric - Invalid (string)",
    lambda: validation.validate_numeric("not a number"),
    should_error=True
)

print("\n\nFLIGHT VALIDATORS")
print("="*60)

# Flight type validation
results.test(
    "Flight type - Valid (Domestic)",
    lambda: validation.validate_flight_type("Domestic"),
    expected_result=True
)

results.test(
    "Flight type - Valid (International)",
    lambda: validation.validate_flight_type("International"),
    expected_result=True
)

results.test(
    "Flight type - Invalid",
    lambda: validation.validate_flight_type("Regional"),
    should_error=True
)

print("\n\nGATE & RUNWAY VALIDATORS")
print("="*60)

# Gate validation
results.test(
    "Gate resource - Valid (A1)",
    lambda: validation.validate_gate("A1"),
    expected_result=True
)

results.test(
    "Gate resource - Valid (B10)",
    lambda: validation.validate_gate("B10"),
    expected_result=True
)

results.test(
    "Gate resource - Invalid",
    lambda: validation.validate_gate("Invalid"),
    should_error=True
)

# Runway validation
results.test(
    "Runway resource - Valid (01L)",
    lambda: validation.validate_runway("01L"),
    expected_result=True
)

results.test(
    "Runway resource - Valid (09R)",
    lambda: validation.validate_runway("09R"),
    expected_result=True
)

results.test(
    "Runway resource - Invalid",
    lambda: validation.validate_runway("XX"),
    should_error=True
)

print("\n\nCREW VALIDATORS")
print("="*60)

# Crew validation
results.test(
    "Crew validation - Valid (Pilot)",
    lambda: validation.validate_crew("Pilot"),
    expected_result=True
)

results.test(
    "Crew validation - Valid (Flight Attendant)",
    lambda: validation.validate_crew("Flight Attendant"),
    expected_result=True
)

results.test(
    "Crew validation - Invalid",
    lambda: validation.validate_crew("Mechanic"),
    should_error=True
)

print("\n\nPASSENGER BOOKING VALIDATION")
print("="*60)

# Passenger booking validation
results.test(
    "Passenger booking - Valid",
    lambda: validation.validate_passenger_booking({"name": "John", "ticket_class": "Economy", "status": "Booked"}),
    expected_result=True
)

results.test(
    "Passenger booking - Missing name",
    lambda: validation.validate_passenger_booking({"ticket_class": "Economy", "status": "Booked"}),
    should_error=True
)

results.test(
    "Passenger booking - Invalid ticket class",
    lambda: validation.validate_passenger_booking({"name": "John", "ticket_class": "Premium", "status": "Booked"}),
    should_error=True
)

print("\n\nCONSTRAINT CHECK HELPERS - DUPLICATES")
print("="*60)

# Duplicate checks
results.test(
    "Check duplicate aircraft - No duplicates",
    lambda: constraint_checking.check_duplicate_aircraft([
        {"aircraft_id": 1, "type": "Boeing 747"},
        {"aircraft_id": 2, "type": "Boeing 777"}
    ]),
    expected_result=True
)

results.test(
    "Check duplicate aircraft - With duplicates",
    lambda: constraint_checking.check_duplicate_aircraft([
        {"aircraft_id": 1, "type": "Boeing 747"},
        {"aircraft_id": 1, "type": "Boeing 747"}
    ]),
    should_error=True
)

results.test(
    "Check duplicate gate - No duplicates",
    lambda: constraint_checking.check_duplicate_gate([
        {"gate": "A1", "type": "International"},
        {"gate": "A2", "type": "Domestic"}
    ]),
    expected_result=True
)

results.test(
    "Check duplicate gate - With duplicates",
    lambda: constraint_checking.check_duplicate_gate([
        {"gate": "A1", "type": "International"},
        {"gate": "A1", "type": "Domestic"}
    ]),
    should_error=True
)

results.test(
    "Check duplicate runway - No duplicates",
    lambda: constraint_checking.check_duplicate_runway([
        {"runway": "01L", "maintenance": False},
        {"runway": "01R", "maintenance": False}
    ]),
    expected_result=True
)

results.test(
    "Check duplicate runway - With duplicates",
    lambda: constraint_checking.check_duplicate_runway([
        {"runway": "01L", "maintenance": False},
        {"runway": "01L", "maintenance": False}
    ]),
    should_error=True
)

results.test(
    "Check duplicate crew - No duplicates",
    lambda: constraint_checking.check_duplicate_crew([
        {"crew_id": 1, "role": "Pilot"},
        {"crew_id": 2, "role": "Flight Attendant"}
    ]),
    expected_result=True
)

results.test(
    "Check duplicate crew - With duplicates",
    lambda: constraint_checking.check_duplicate_crew([
        {"crew_id": 1, "role": "Pilot"},
        {"crew_id": 1, "role": "Pilot"}
    ]),
    should_error=True
)

print("\n\nCONSTRAINT CHECK HELPERS - CONFLICTS")
print("="*60)

# Conflict checks
results.test(
    "Check runway maintenance consistency - Valid",
    lambda: constraint_checking.check_runway_maintenance_consistency([
        {"runway": "01L", "maintenance": False, "status": "Available"},
        {"runway": "01R", "maintenance": True, "status": "Under Maintenance"}
    ]),
    expected_result=True
)

results.test(
    "Check runway maintenance consistency - Conflict",
    lambda: constraint_checking.check_runway_maintenance_consistency([
        {"runway": "01L", "maintenance": False, "status": "Under Maintenance"}
    ]),
    should_error=True
)

print("\n\nGATE CONSTRAINT CHECKS")
print("="*60)

# Gate constraint checks
results.test(
    "Check gate constraints - Valid (International gate available)",
    lambda: constraint_checking.check_gate_constraints(
        {"gate": "A1", "type": "International", "size": "Large"},
        "Available"
    ),
    expected_result=True
)

results.test(
    "Check gate constraints - Valid (Domestic gate available)",
    lambda: constraint_checking.check_gate_constraints(
        {"gate": "B5", "type": "Domestic", "size": "Medium"},
        "Available"
    ),
    expected_result=True
)

results.test(
    "Check gate constraints - Unavailable gate",
    lambda: constraint_checking.check_gate_constraints(
        {"gate": "A1", "type": "International", "size": "Large"},
        "Occupied"
    ),
    should_error=True
)

print("\n\nRUNWAY CONSTRAINT CHECKS")
print("="*60)

# Runway constraint checks
results.test(
    "Check runway constraints - Valid (Available, not in maintenance)",
    lambda: constraint_checking.check_runway_constraints(
        {"runway": "01L", "maintenance": False},
        "Available"
    ),
    expected_result=True
)

results.test(
    "Check runway constraints - Under maintenance",
    lambda: constraint_checking.check_runway_constraints(
        {"runway": "01L", "maintenance": True},
        "Under Maintenance"
    ),
    should_error=True
)

print("\n\nCREW CONSTRAINT CHECKS")
print("="*60)

# Crew constraint checks
results.test(
    "Check crew constraints - Valid (Available, within hours)",
    lambda: constraint_checking.check_crew_constraints(
        {"crew_id": 1, "role": "Pilot"},
        "Available",
        5  # 5 hours flight time
    ),
    expected_result=True
)

results.test(
    "Check crew constraints - Exceeds max hours",
    lambda: constraint_checking.check_crew_constraints(
        {"crew_id": 1, "role": "Pilot"},
        "Available",
        12  # exceeds typical max
    ),
    should_error=True
)

print("\n\nFLIGHT CONSTRAINT CHECKS")
print("="*60)

# Flight constraint checks
results.test(
    "Check flight constraints - Valid",
    lambda: constraint_checking.validate_flight_constraints({
        "flight_id": "AA100",
        "aircraft": "Boeing 747",
        "gate": "A1",
        "runway": "01L",
        "crew": {"pilot": 1, "attendants": 5}
    }),
    expected_result=True
)

results.test(
    "Check aircraft constraints - Valid",
    lambda: constraint_checking.check_aircraft_constraints(
        {"aircraft_id": 1, "type": "Boeing 747", "status": "Available"},
        "Available"
    ),
    expected_result=True
)

results.test(
    "Check aircraft constraints - Not available",
    lambda: constraint_checking.check_aircraft_constraints(
        {"aircraft_id": 1, "type": "Boeing 747", "status": "Maintenance"},
        "Maintenance"
    ),
    should_error=True
)

print("\n\nPASSENGER CONSTRAINT CHECKS")
print("="*60)

# Passenger constraint checks
results.test(
    "Check passenger constraints - Valid",
    lambda: constraint_checking.check_passenger_constraints(
        {"passenger_id": 1, "name": "John", "status": "Booked", "seat": "1A"},
        "Booked"
    ),
    expected_result=True
)

results.test(
    "Check passenger constraints - Boarded",
    lambda: constraint_checking.check_passenger_constraints(
        {"passenger_id": 1, "name": "John", "status": "Boarded", "seat": "1A"},
        "Boarded"
    ),
    expected_result=True
)

print("\n\nDISRUPTION CONSTRAINT CHECKS")
print("="*60)

# Disruption constraint checks
results.test(
    "Check disruption constraints - Valid (Active)",
    lambda: constraint_checking.check_disruption_constraints(
        {"disruption_id": 1, "type": "Weather", "status": "Active", "priority": "High"},
        "Active"
    ),
    expected_result=True
)

results.test(
    "Check disruption constraints - Resolved",
    lambda: constraint_checking.check_disruption_constraints(
        {"disruption_id": 1, "type": "Weather", "status": "Resolved", "priority": "Low"},
        "Resolved"
    ),
    expected_result=True
)

# Print summary
results.summary()

# Exit with appropriate code
sys.exit(0 if results.failed == 0 else 1)
