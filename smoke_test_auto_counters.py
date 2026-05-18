# Smoke test: auto-create counters when demand exceeds capacity
from pathlib import Path

# Create minimal data files for allocation
base = Path('.')

base.joinpath('aircraft.csv').write_text('A1,Wide,Airport,No,30\n')
base.joinpath('gates.csv').write_text('G1,T1,Domestic,Wide,Free\n')
base.joinpath('runwaydetails.csv').write_text('4000,Free,NA,R1,Regular,No,NA,NA\n')
base.joinpath('crew.csv').write_text('C1,John,Pilot,NA,Morning,Wide,Available,0,12\nC2,Mary,Attendant,NA,Evening,Wide,Available,0,12\n')
base.joinpath('ground_resources.csv').write_text('R1,Loader,Available\nR2,PushBack,Available\nR3,Tug,Available\n')
# start with no counters to force auto-creation
if base.joinpath('counters.csv').exists():
    base.joinpath('counters.csv').write_text('')

# Flight with capacity 120
base.joinpath('flights.csv').write_text('F1,TestAir,AAA,BBB,1000,1100,01-01-2026,NA,Domestic,120\n')

# Create 120 passengers for flight F1
lines = []
for i in range(1,121):
    pid = f'P{i}'
    name = f'Passenger{i}'
    fno = 'F1'
    seat = f'{i}A'
    lines.append(','.join([pid, name, fno, seat, 'Economy', 'Booked', 'NA']))
base.joinpath('passenger.csv').write_text('\n'.join(lines) + '\n')

# Remove any existing allocations
if base.joinpath('flight_allocations.csv').exists():
    base.joinpath('flight_allocations.csv').unlink()

print('Files created. Running allocation...')

# Run allocation
from flights import load_flights
from allocation_engine import allocate_flight

flights = load_flights()
flight = next((f for f in flights if f.fno == 'F1'), None)
if not flight:
    print('Flight F1 not found')
else:
    allocate_flight(flight)

# Show results
print('\n--- Allocation Output ---')
if Path('flight_allocations.csv').exists():
    print(Path('flight_allocations.csv').read_text())
else:
    print('No allocations file')

print('\n--- counters.csv ---')
print(Path('counters.csv').read_text())

print('\n--- passengers assigned counters (first 5) ---')
from passenger import load_passengers
ps = [p for p in load_passengers() if p.fno == 'F1']
for p in ps[:5]:
    print(p.pid, p.name, p.counter_id)

print('\nSmoke test completed.')
