# Automated smoke tests for counters and booking flow
import sys
from pathlib import Path
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE = Path(__file__).parent.parent

def setup_environment():
    BASE.joinpath('aircraft.csv').write_text('A1,Wide,Airport,No,30\n')
    BASE.joinpath('gates.csv').write_text('G1,T1,Domestic,Wide,Free\n')
    BASE.joinpath('runwaydetails.csv').write_text('4000,Free,NA,R1,Both,No,NA,NA\n')
    BASE.joinpath('crew.csv').write_text('C1,John,Pilot,NA,Morning,Wide,Available,0,12\nC2,Mary,Attendant,NA,Evening,Wide,Available,0,12\n')
    BASE.joinpath('ground_resources.csv').write_text('R1,Loader,Available\nR2,PushBack,Available\nR3,Tug,Available\n')
    # ensure counters file is empty
    BASE.joinpath('counters.csv').write_text('')
    BASE.joinpath('flights.csv').write_text('F1,TestAir,AAA,BBB,1000,1100,01-01-2026,NA,Domestic,120\n')
    # passengers
    lines = []
    for i in range(1,121):
        pid = f'P{i}'
        name = f'Passenger{i}'
        fno = 'F1'
        seat = f'{i}A'
        lines.append(','.join([pid, name, fno, seat, 'Economy', 'Booked', 'NA']))
    BASE.joinpath('passenger.csv').write_text('\n'.join(lines) + '\n')
    if BASE.joinpath('flight_allocations.csv').exists():
        BASE.joinpath('flight_allocations.csv').unlink()


def run_allocation():
    from flights import load_flights
    from allocation_engine import allocate_flight
    flights = load_flights()
    flight = next((f for f in flights if f.fno == 'F1'), None)
    if not flight:
        raise RuntimeError('Flight F1 missing')
    allocate_flight(flight)


def assertions():
    # flight_allocations.csv must exist
    fa = BASE.joinpath('flight_allocations.csv')
    assert fa.exists(), 'flight_allocations.csv not created'
    content = fa.read_text()
    assert 'F1,' in content, 'Allocation for F1 missing'

    # counters.csv should have been auto-created
    counters = BASE.joinpath('counters.csv').read_text().strip().splitlines()
    assert len(counters) >= 2, f'Expected at least 2 counters, found {len(counters)}'
    # check counters occupancy
    occ = [line for line in counters if line.strip().endswith('Occupied')]
    assert len(occ) >= 1, 'No counters marked Occupied after allocation'

    # passengers should have counter assignments
    ps = BASE.joinpath('passenger.csv').read_text().strip().splitlines()
    assert len(ps) >= 120, 'Passenger rows missing'
    first = ps[0].split(',')
    assert len(first) >= 7, 'Passenger row format unexpected'
    counter_field = first[6]
    assert counter_field != 'NA' and counter_field != '', 'Passengers not assigned counters'


def main():
    print('Setting up test environment...')
    setup_environment()
    print('Running allocation...')
    run_allocation()
    print('Verifying results...')
    assertions()
    print('SMOKE TESTS PASSED')

if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        print('SMOKE TEST FAILED:', e)
        sys.exit(2)
    except Exception as e:
        print('ERROR DURING TEST:', e)
        sys.exit(3)
