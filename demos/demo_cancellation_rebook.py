from pathlib import Path
# Setup minimal environment
BASE = Path(__file__).parents[1]

BASE.joinpath('aircraft.csv').write_text('A1,Wide,Airport,No,30\n')
BASE.joinpath('gates.csv').write_text('G1,T1,Domestic,Wide,Free\n')
BASE.joinpath('runwaydetails.csv').write_text('4000,Free,NA,R1,Both,No,NA,NA\n')
BASE.joinpath('crew.csv').write_text('C1,John,Pilot,NA,Morning,Wide,Available,0,12\nC2,Mary,Attendant,NA,Evening,Wide,Available,0,12\n')
BASE.joinpath('ground_resources.csv').write_text('R1,Loader,Available\nR2,PushBack,Available\nR3,Tug,Available\n')
# start with empty counters (auto-create will happen)
BASE.joinpath('counters.csv').write_text('')

# Flights: F1 (to be cancelled) and F2 (alternative)
BASE.joinpath('flights.csv').write_text('\n'.join([
    'F1,TestAir,AAA,BBB,1000,1100,01-01-2026,NA,Domestic,120',
    'F2,TestAir,AAA,BBB,1200,1300,01-01-2026,NA,Domestic,120'
]) + '\n')

# Passengers on F1
lines = []
for i in range(1,4):
    lines.append(','.join([f'P{i}', f'Passenger{i}', 'F1', f'{i}A', 'Economy', 'Booked', 'NA']))
BASE.joinpath('passenger.csv').write_text('\n'.join(lines) + '\n')

# ensure no allocations present
fa = BASE.joinpath('flight_allocations.csv')
if fa.exists():
    fa.unlink()

print('Environment ready — allocating F1')

from flights import load_flights
from allocation_engine import allocate_flight
fl = load_flights()
f1 = next((f for f in fl if f.fno == 'F1'), None)
allocate_flight(f1)

print('\nNow cancelling F1 and offering rebooking (simulated responses)')

import builtins
# For each passenger we will answer 'yes' then choose 'F2'
# 3 passengers → 6 inputs: yes,F2 repeated
responses = iter(['yes','F2'] * 3)
orig_input = builtins.input
builtins.input = lambda prompt='': next(responses)

try:
    from allocation_engine import handle_cancellation
    handle_cancellation('F1')
finally:
    builtins.input = orig_input

print('\nFinal passenger.csv:')
print(BASE.joinpath('passenger.csv').read_text())

print('Demo complete.')
