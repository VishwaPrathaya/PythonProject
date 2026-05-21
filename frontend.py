import html
from pathlib import Path
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs

from allocation_engine import (
    allocate_flight,
    handle_cancellation,
    handle_delay,
    try_schedule_pending_flights,
    release_expired_allocations,
    system_rebalance,
    get_recent_allocation_errors,
    get_last_allocation_error,
)
from conflict_resolution import resolve_conflicts
from passenger_allocation import allocate_passengers
import disruption_details
import flights
import counters
import passenger
import aircraft
import gates
import runways
import crew
import ground_resources
from passenger import seats_used
from validation import (
    validate_flight,
    validate_numeric,
    validate_flight_type,
    validate_passenger_booking,
    validate_ticket_class,
    validate_passenger_status,
    validate_disruption,
    validate_disruption_type,
    validate_disruption_status,
    validate_priority,
    validate_aircraft,
    validate_aircraft_fields,
    validate_crew,
    validate_crew_hours,
    validate_gate,
    validate_runway,
    validate_resource,
)
from constraint_checking import validate_flight_constraints, get_last_constraint_error


def render_page(title, body, message=None):
    nav = (
        '<nav class="topbar">'
        '<a href="/">Dashboard</a>'
        '<a href="/flights">Flights</a>'
        '<a href="/passengers">Passengers</a>'
        '<a href="/counters">Counters</a>'
        '<a href="/aircraft">Aircraft</a>'
        '<a href="/crew">Crew</a>'
        '<a href="/gates">Gates</a>'
        '<a href="/runways">Runways</a>'
        '<a href="/resources">Resources</a>'
        '<a href="/disruptions">Disruptions</a>'
        '<a href="/notifications">Notifications</a>'
        '<a href="/actions">Actions</a>'
        '</nav>'
    )
    status = f'<p class="status">{html.escape(message)}</p>' if message else ''
    page = (
        '<!DOCTYPE html><html><head><meta charset="utf-8">'
        f'<title>{html.escape(title)}</title>'
        '<style>'
        'body{font-family:Inter,system-ui,Arial,sans-serif;padding:0;margin:0;background:#f5f8fb;color:#1f2937;}'
        'header{padding:24px;max-width:1200px;margin:0 auto;}'
        '.topbar{display:flex;flex-wrap:wrap;gap:10px;padding:16px 24px;margin:0 auto 24px;max-width:1200px;}'
        '.topbar a{padding:10px 14px;border-radius:9999px;background:rgba(59,130,246,0.12);color:#1d4ed8;text-decoration:none;font-size:0.95rem;transition:background 0.2s;}'
        '.topbar a:hover{background:rgba(59,130,246,0.2);}'
        'main{max-width:1200px;margin:0 auto;padding:0 24px 32px;}'
        'h1{margin:0;font-size:2rem;color:#0f172a;}'
        '.status{margin:16px 0;padding:14px 18px;background:#ecfdf5;color:#166534;border:1px solid #bbf7d0;border-radius:10px;}'
        'section{background:#ffffff;border:1px solid #e2e8f0;border-radius:18px;padding:24px;box-shadow:0 16px 50px rgba(15,23,42,0.06);margin-bottom:24px;}'
        '.hero{padding:28px;border-radius:18px;background:linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);color:#ffffff;margin-bottom:24px;}'
        '.hero p{opacity:.88;line-height:1.8;max-width:760px;}'
        '.metric-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;margin-top:18px;}'
        '.metric-card{background:#f8fafc;border:1px solid #e2e8f0;border-radius:18px;padding:18px;}'
        '.metric-card h3{margin:0 0 10px;font-size:1.05rem;color:#0f172a;}'
        '.metric-card p{font-size:2rem;margin:0;color:#1d4ed8;}'
        '.metric-card small{color:#475569;}'
        '.card-actions{display:grid;gap:12px;margin-top:24px;}'
        '.card-actions a{display:inline-flex;align-items:center;justify-content:center;padding:14px 18px;border-radius:14px;text-decoration:none;font-weight:600;}'
        '.primary-btn{background:#2563eb;color:#fff;}'
        '.secondary-btn{background:#e2e8f0;color:#1f2937;}'
        'table{border-collapse:collapse;width:100%;margin-top:16px;font-size:0.95rem;}'
        'th,td{border:1px solid #e2e8f0;padding:12px;text-align:left;}'
        'th{background:#f1f5f9;color:#0f172a;}'
        'tr:nth-child(even){background:#f8fafc;}'
        'input,select,button,textarea{width:100%;padding:12px;margin:8px 0;border:1px solid #cbd5e0;border-radius:12px;font-size:0.95rem;box-sizing:border-box;}'
        'button{cursor:pointer;transition:filter 0.2s;}'
        'button:hover{filter:brightness(1.05);}'
        '</style>'
        '</head><body>'
        '<header>'
        f'<h1>{html.escape(title)}</h1>'
        f'{status}'
        '</header>'
        f'{nav}'
        '<main><section>'
        f'{body}'
        '</section></main>'
        '</body></html>'
    )
    return page


def response(start_response, content, status='200 OK'):
    start_response(status, [('Content-type', 'text/html; charset=utf-8')])
    return [content.encode('utf-8')]


def parse_post(environ):
    try:
        size = int(environ.get('CONTENT_LENGTH', '0') or '0')
    except ValueError:
        size = 0
    data = environ['wsgi.input'].read(size) if size > 0 else b''
    return {k: v[0] for k, v in parse_qs(data.decode('utf-8')).items()}


def table_from_objects(headers, rows):
    cells = ''.join(f'<th>{html.escape(h)}</th>' for h in headers)
    body = ''.join('<tr>' + ''.join(f'<td>{html.escape(str(c))}</td>' for c in row) + '</tr>' for row in rows)
    return f'<table><thead><tr>{cells}</tr></thead><tbody>{body}</tbody></table>'


def allocation_errors_table(errors):
    if not errors:
        return '<h2>Recent Allocation Failures</h2><p>No recent allocation failures.</p>'
    rows = [[entry['time'], entry['flight'], entry['reason']] for entry in errors]
    return '<h2>Recent Allocation Failures</h2>' + table_from_objects(['Time', 'Flight', 'Reason'], rows)


def home_page(message=None):
    flight_count = len(flights.load_flights())
    passenger_count = len(passenger.load_passengers())
    counter_count = len(counters.load_counters())
    aircraft_count = len(aircraft.load_aircraft())
    crew_count = len(crew.load_crew())
    gate_count = len(gates.load_gates())
    runway_count = len(runways.load_runways())
    resource_count = len(ground_resources.load_resources())
    errors = get_recent_allocation_errors(5)
    content = (
        '<div class="hero">'
        '<h2>Airport Operations Dashboard</h2>'
        '<p>Track daily flights, manage airport resources, and resolve disruptions from a single interface.</p>'
        '</div>'
        '<div class="metric-grid">'
        f'<div class="metric-card"><h3>Flights</h3><p>{flight_count}</p><small>Schedule entries</small></div>'
        f'<div class="metric-card"><h3>Passengers</h3><p>{passenger_count}</p><small>Active bookings</small></div>'
        f'<div class="metric-card"><h3>Counters</h3><p>{counter_count}</p><small>Service counters</small></div>'
        f'<div class="metric-card"><h3>Aircraft</h3><p>{aircraft_count}</p><small>Aircraft profiles</small></div>'
        f'<div class="metric-card"><h3>Crew</h3><p>{crew_count}</p><small>Crew records</small></div>'
        f'<div class="metric-card"><h3>Gates</h3><p>{gate_count}</p><small>Gate resources</small></div>'
        f'<div class="metric-card"><h3>Runways</h3><p>{runway_count}</p><small>Runway entries</small></div>'
        f'<div class="metric-card"><h3>Resources</h3><p>{resource_count}</p><small>Support equipment</small></div>'
        f'<div class="metric-card"><h3>Recent Failures</h3><p>{len(errors)}</p><small>Allocation issues</small></div>'
        '</div>'
        f'{allocation_errors_table(errors)}'
        '<div class="card-actions">'
        '<a class="primary-btn" href="/actions">Run System Actions</a>'
        '<a class="secondary-btn" href="/notifications">View Notifications</a>'
        '</div>'
    )
    return render_page('Airport Operations Dashboard', content, message)


def all_flights_page(params=None, message=None):
    flights_list = flights.load_flights()
    rows = [[f.fno, f.airline, f.origin, f.destination, f.arr, f.dep, f.date, f.aircraft, f.flight_type, f.capacity] for f in flights_list]
    content = '<h2>Flights</h2>' + table_from_objects(['FNO', 'Airline', 'Origin', 'Destination', 'Arr', 'Dep', 'Date', 'Aircraft', 'Type', 'Capacity'], rows)
    content += (
        '<h3>Add Flight</h3>'
        '<form method="post">'
        '<input type="hidden" name="action" value="add_flight">'
        'Flight No:<br><input name="fno"><br>'
        'Airline:<br><input name="airline"><br>'
        'Origin:<br><input name="origin"><br>'
        'Destination:<br><input name="destination"><br>'
        'Arrival:<br><input name="arr"><br>'
        'Departure:<br><input name="dep"><br>'
        'Date:<br><input name="date"><br>'
        'Type:<br><select name="flight_type"><option>Domestic</option><option>International</option></select><br>'
        'Capacity:<br><input name="capacity" value="100"><br>'
        '<button type="submit">Add Flight</button>'
        '</form>'
    )
    content += '<h3>Manual Allocation</h3>'
    content += '<form method="post"><input type="hidden" name="action" value="allocate_flight">Flight ID:<br><input name="fno"><br><button type="submit">Allocate Flight</button></form>'
    return render_page('Flight Management', content, message)


def handle_add_flight(params):
    fno = params.get('fno', '').strip()
    airline = params.get('airline', '').strip()
    origin = params.get('origin', '').strip()
    destination = params.get('destination', '').strip()
    arr = params.get('arr', '').strip()
    dep = params.get('dep', '').strip()
    date = params.get('date', '').strip()
    flight_type = params.get('flight_type', 'Domestic').strip()
    capacity = params.get('capacity', '100').strip()

    existing = flights.load_flights()
    if not validate_flight(fno, arr, dep, flight_type, date, existing):
        return False, 'Flight validation failed'
    if not validate_flight_constraints(existing, fno, int(arr), int(dep)):
        reason = get_last_constraint_error() or 'Flight constraint violation'
        return False, f'Flight constraint violation: {reason}'
    if not capacity.isdigit():
        return False, 'Capacity must be numeric'

    with open('flights.csv', 'a', encoding='utf-8') as f:
        f.write(','.join([fno, airline, origin, destination, arr, dep, date, 'NA', flight_type, capacity]) + '\n')

    allocate_flight(next((fl for fl in flights.load_flights() if fl.fno == fno), None))
    last_error = get_last_allocation_error()
    if last_error:
        return False, f'Allocation failed: {last_error["reason"]}'
    return True, f'Flight {fno} added and allocation attempted.'


def handle_allocate_flight(params):
    fno = params.get('fno', '').strip()
    flight = next((fl for fl in flights.load_flights() if fl.fno == fno), None)
    if not flight:
        return False, 'Flight not found'
    allocate_flight(flight)
    last_error = get_last_allocation_error()
    if last_error:
        return False, f'Allocation failed: {last_error["reason"]}'
    return True, f'Allocation attempted for {fno}.'


def counters_page(params=None, message=None):
    counters_list = counters.load_counters()
    rows = [[c.counter_id, c.gate_id, c.terminal, c.service_type, c.availability, c.capacity] for c in counters_list]
    content = '<h2>Counters</h2>' + table_from_objects(['ID', 'Gate', 'Terminal', 'Service', 'Availability', 'Capacity'], rows)
    content += (
        '<h3>Add Counter</h3>'
        '<form method="post">'
        '<input type="hidden" name="action" value="add_counter">'
        'Counter ID:<br><input name="counter_id"><br>'
        'Gate ID:<br><input name="gate_id"><br>'
        'Terminal:<br><input name="terminal"><br>'
        'Service Type:<br><select name="service_type"><option>Check-In</option><option>Boarding</option></select><br>'
        'Availability:<br><select name="availability"><option>Available</option><option>Occupied</option></select><br>'
        'Capacity:<br><input name="capacity" value="50"><br>'
        '<button type="submit">Add Counter</button>'
        '</form>'
    )
    return render_page('Counter Management', content, message)


def handle_add_counter(params):
    counter_id = params.get('counter_id', '').strip()
    gate_id = params.get('gate_id', '').strip()
    terminal = params.get('terminal', '').strip()
    service_type = params.get('service_type', 'Check-In').strip()
    availability = params.get('availability', 'Available').strip()
    capacity = params.get('capacity', '50').strip()
    if not capacity.isdigit():
        return False, 'Capacity must be numeric'
    counter = counters.create_counter(counter_id, gate_id, terminal, service_type, availability, int(capacity))
    if not counter:
        return False, 'Counter creation failed (duplicate or invalid fields)'
    return True, f'Counter {counter_id} added.'


def passengers_page(params=None, message=None):
    passenger_list = passenger.load_passengers()
    rows = [[p.pid, p.name, p.fno, p.seat, p.ticket_class, p.status, p.counter_id] for p in passenger_list]
    content = '<h2>Passengers</h2>' + table_from_objects(['ID', 'Name', 'Flight', 'Seat', 'Class', 'Status', 'Counter'], rows)
    content += (
        '<h3>Book Passenger</h3>'
        '<form method="post">'
        '<input type="hidden" name="action" value="book_passenger">'
        'Passenger ID:<br><input name="pid"><br>'
        'Name:<br><input name="name"><br>'
        'Flight No:<br><input name="fno"><br>'
        'Seat:<br><input name="seat"><br>'
        'Class:<br><select name="ticket_class"><option>Economy</option><option>Business</option><option>First</option></select><br>'
        'Status:<br><select name="status"><option>Booked</option><option>Checked-In</option><option>Boarded</option></select><br>'
        '<button type="submit">Book Passenger</button>'
        '</form>'
    )
    return render_page('Passenger Booking', content, message)


def handle_book_passenger(params):
    pid = params.get('pid', '').strip()
    name = params.get('name', '').strip()
    fno = params.get('fno', '').strip()
    seat = params.get('seat', '').strip()
    ticket_class = params.get('ticket_class', 'Economy').strip()
    status = params.get('status', 'Booked').strip()
    selected = next((f for f in flights.load_flights() if f.fno == fno), None)
    existing = passenger.load_passengers()

    if not selected:
        return False, 'Flight not found'
    if not validate_ticket_class(ticket_class):
        return False, 'Invalid ticket class'
    if not validate_passenger_status(status):
        return False, 'Invalid passenger status'
    if not validate_passenger_booking(pid, name, selected, seat, existing, seats_used):
        return False, 'Passenger booking validation failed'

    with open('passenger.csv', 'a', encoding='utf-8') as f:
        f.write(','.join([pid, name, fno, seat, ticket_class, status, 'NA']) + '\n')

    allocate_passengers()
    return True, f'Passenger {pid} booked on flight {fno}.'


def aircraft_page(params=None, message=None):
    aircraft_list = aircraft.load_aircraft()
    rows = [[a.aircraft_id, a.atype, a.location, a.maintenance, a.turnaround_time] for a in aircraft_list]
    content = '<h2>Aircraft</h2>' + table_from_objects(['ID', 'Type', 'Location', 'Maintenance', 'TAT'], rows)
    content += (
        '<h3>Add Aircraft</h3>'
        '<form method="post">'
        '<input type="hidden" name="action" value="add_aircraft">'
        'Aircraft ID:<br><input name="aid"><br>'
        'Type:<br><select name="atype"><option>Wide</option><option>Narrow</option></select><br>'
        'Location:<br><select name="location"><option>Airport</option><option>Other</option></select><br>'
        'Maintenance:<br><select name="maintenance"><option>No</option><option>Yes</option></select><br>'
        'Turnaround Time:<br><input name="tat"><br>'
        '<button type="submit">Add Aircraft</button>'
        '</form>'
    )
    return render_page('Aircraft Management', content, message)


def handle_add_aircraft(params):
    aid = params.get('aid', '').strip()
    atype = params.get('atype', '').strip()
    location = params.get('location', '').strip()
    maintenance = params.get('maintenance', '').strip()
    tat = params.get('tat', '').strip()

    if not validate_aircraft(aid, atype):
        return False, 'Invalid aircraft ID or type'
    if not validate_aircraft_fields(atype, maintenance, tat):
        return False, 'Invalid aircraft data'

    existing = aircraft.load_aircraft()
    if any(a.aircraft_id == aid for a in existing):
        return False, 'Duplicate aircraft ID'

    with open('aircraft.csv', 'a', encoding='utf-8') as f:
        f.write(','.join([aid, atype, location, maintenance, tat]) + '\n')

    return True, f'Aircraft {aid} added.'


def crew_page(params=None, message=None):
    crew_list = crew.load_crew()
    rows = [[c.crew_id, c.name, c.role, c.flight_no, c.shift, c.aircraft_type, c.status, c.duty_hours, c.rest_hours] for c in crew_list]
    content = '<h2>Crew</h2>' + table_from_objects(['ID', 'Name', 'Role', 'Flight', 'Shift', 'Aircraft Type', 'Status', 'Duty', 'Rest'], rows)
    content += (
        '<h3>Add Crew</h3>'
        '<form method="post">'
        '<input type="hidden" name="action" value="add_crew">'
        'Crew ID:<br><input name="cid"><br>'
        'Name:<br><input name="name"><br>'
        'Role:<br><select name="role"><option>Pilot</option><option>Co-Pilot</option><option>Cabin Crew</option></select><br>'
        'Flight No:<br><input name="fno" value="NA"><br>'
        'Shift:<br><input name="shift"><br>'
        'Aircraft Type:<br><select name="atype"><option>Wide</option><option>Narrow</option></select><br>'
        'Status:<br><select name="status"><option>Available</option><option>Assigned</option></select><br>'
        'Duty Hours:<br><input name="duty"><br>'
        'Rest Hours:<br><input name="rest"><br>'
        '<button type="submit">Add Crew</button>'
        '</form>'
    )
    return render_page('Crew Management', content, message)


def handle_add_crew(params):
    cid = params.get('cid', '').strip()
    name = params.get('name', '').strip()
    role = params.get('role', '').strip()
    fno = params.get('fno', 'NA').strip() or 'NA'
    shift = params.get('shift', '').strip()
    atype = params.get('atype', '').strip()
    status = params.get('status', 'Available').strip()
    duty = params.get('duty', '').strip()
    rest = params.get('rest', '').strip()

    if not validate_crew(cid, name, role):
        return False, 'Invalid crew data'
    if not validate_crew_hours(duty, rest):
        return False, 'Invalid duty/rest values'

    existing = crew.load_crew()
    if any(c.crew_id == cid for c in existing):
        return False, 'Duplicate crew ID'

    with open('crew.csv', 'a', encoding='utf-8') as f:
        f.write(','.join([cid, name, role, fno, shift, atype, status, duty, rest]) + '\n')

    return True, f'Crew {cid} added.'


def gates_page(params=None, message=None):
    gate_list = gates.load_gates()
    rows = [[g.gate_id, g.terminal, g.gate_type, g.max_aircraft_size, g.availability] for g in gate_list]
    content = '<h2>Gates</h2>' + table_from_objects(['Gate', 'Terminal', 'Type', 'Size', 'Availability'], rows)
    content += (
        '<h3>Add Gate</h3>'
        '<form method="post">'
        '<input type="hidden" name="action" value="add_gate">'
        'Gate ID:<br><input name="gid"><br>'
        'Terminal:<br><input name="terminal"><br>'
        'Gate Type:<br><select name="gtype"><option>Domestic</option><option>International</option></select><br>'
        'Size:<br><select name="size"><option>Wide</option><option>Narrow</option></select><br>'
        'Availability:<br><select name="availability"><option>Free</option><option>Occupied</option></select><br>'
        '<button type="submit">Add Gate</button>'
        '</form>'
    )
    return render_page('Gate Management', content, message)


def handle_add_gate(params):
    gid = params.get('gid', '').strip()
    terminal = params.get('terminal', '').strip()
    gtype = params.get('gtype', '').strip()
    size = params.get('size', '').strip()
    availability = params.get('availability', 'Free').strip()

    if not validate_gate(gid, gtype, size, availability):
        return False, 'Invalid gate data'

    existing = gates.load_gates()
    if any(g.gate_id == gid for g in existing):
        return False, 'Duplicate gate ID'

    with open('gates.csv', 'a', encoding='utf-8') as f:
        f.write(','.join([gid, terminal, gtype, size, availability]) + '\n')

    return True, f'Gate {gid} added.'


def runways_page(params=None, message=None):
    runway_list = runways.load_runways()
    rows = [[r.runway_id, r.length, r.availability, r.assigned_flight, r.usage, r.maintenance_window, r.maintenance_from, r.maintenance_to] for r in runway_list]
    content = '<h2>Runways</h2>' + table_from_objects(['ID', 'Length', 'Availability', 'Flight', 'Usage', 'Maintenance', 'From', 'To'], rows)
    content += (
        '<h3>Add Runway</h3>'
        '<form method="post">'
        '<input type="hidden" name="action" value="add_runway">'
        'Runway ID:<br><input name="rid"><br>'
        'Length:<br><input name="length"><br>'
        'Availability:<br><select name="availability"><option>Free</option><option>Occupied</option></select><br>'
        'Usage:<br><select name="usage"><option>Takeoff</option><option>Landing</option><option>Both</option></select><br>'
        'Maintenance Window:<br><select name="maintenance_window"><option>No</option><option>Yes</option></select><br>'
        'Maintenance From:<br><input name="maintenance_from" value="NA"><br>'
        'Maintenance To:<br><input name="maintenance_to" value="NA"><br>'
        '<button type="submit">Add Runway</button>'
        '</form>'
    )
    return render_page('Runway Management', content, message)


def handle_add_runway(params):
    rid = params.get('rid', '').strip()
    length = params.get('length', '').strip()
    availability = params.get('availability', 'Free').strip()
    usage = params.get('usage', '').strip()
    maintenance_window = params.get('maintenance_window', 'No').strip()
    maintenance_from = params.get('maintenance_from', 'NA').strip() or 'NA'
    maintenance_to = params.get('maintenance_to', 'NA').strip() or 'NA'

    if not validate_runway(length, availability, usage, maintenance_window):
        return False, 'Invalid runway data'

    existing = runways.load_runways()
    if any(r.runway_id == rid for r in existing):
        return False, 'Duplicate runway ID'

    with open('runwaydetails.csv', 'a', encoding='utf-8') as f:
        f.write(','.join([length, availability, 'NA', rid, usage, maintenance_window, maintenance_from, maintenance_to]) + '\n')

    return True, f'Runway {rid} added.'


def resources_page(params=None, message=None):
    resources_list = ground_resources.load_resources()
    rows = [[r.res_id, r.res_type, r.status] for r in resources_list]
    content = '<h2>Ground Resources</h2>' + table_from_objects(['ID', 'Type', 'Status'], rows)
    content += (
        '<h3>Add Resource</h3>'
        '<form method="post">'
        '<input type="hidden" name="action" value="add_resource">'
        'Resource ID:<br><input name="res_id"><br>'
        'Resource Type:<br><input name="res_type"><br>'
        'Status:<br><select name="status"><option>Available</option><option>In Use</option></select><br>'
        '<button type="submit">Add Resource</button>'
        '</form>'
    )
    return render_page('Ground Resource Management', content, message)


def handle_add_resource(params):
    res_id = params.get('res_id', '').strip()
    res_type = params.get('res_type', '').strip()
    status = params.get('status', 'Available').strip()

    if not validate_resource(res_id, res_type, status):
        return False, 'Invalid resource data'

    existing = ground_resources.load_resources()
    if any(r.res_id == res_id for r in existing):
        return False, 'Duplicate resource ID'

    with open('ground_resources.csv', 'a', encoding='utf-8') as f:
        f.write(','.join([res_id, res_type, status]) + '\n')

    return True, f'Resource {res_id} added.'


def disruptions_page(params=None, message=None):
    disruptions = disruption_details.load_disruptions()
    rows = [[d.disruption_id, d.flight_no, d.disruption_type, d.status, d.priority] for d in disruptions]
    content = '<h2>Disruptions</h2>' + table_from_objects(['ID', 'Flight', 'Type', 'Status', 'Priority'], rows)
    content += (
        '<h3>Add Disruption</h3>'
        '<form method="post">'
        '<input type="hidden" name="action" value="add_disruption">'
        'Disruption ID:<br><input name="disruption_id"><br>'
        'Flight No:<br><input name="flight_no"><br>'
        'Type:<br><select name="disruption_type"><option>Delay</option><option>Technical</option><option>Weather</option><option>Cancellation</option></select><br>'
        'Status:<br><select name="status"><option>Pending</option><option>Resolved</option></select><br>'
        'Priority:<br><select name="priority"><option>High</option><option>Medium</option><option>Low</option></select><br>'
        '<button type="submit">Add Disruption</button>'
        '</form>'
    )
    return render_page('Disruption Management', content, message)


def handle_add_disruption(params):
    disruption_id = params.get('disruption_id', '').strip()
    flight_no = params.get('flight_no', '').strip()
    disruption_type = params.get('disruption_type', '').strip()
    status = params.get('status', '').strip()
    priority = params.get('priority', '').strip()

    if not validate_disruption(disruption_id, flight_no, disruption_type, status):
        return False, 'Invalid disruption data'
    if not validate_disruption_type(disruption_type):
        return False, 'Invalid disruption type'
    if not validate_disruption_status(status):
        return False, 'Invalid disruption status'
    if not validate_priority(priority):
        return False, 'Invalid priority'

    with open('disruption.csv', 'a', encoding='utf-8') as f:
        f.write(','.join([disruption_id, flight_no, disruption_type, status, priority]) + '\n')

    if disruption_type == 'Cancellation':
        handle_cancellation(flight_no)
        return True, f'Cancellation recorded and resources released for {flight_no}.'
    if disruption_type == 'Delay':
        handle_delay(flight_no)
        return True, f'Delay recorded and flight {flight_no} will be rescheduled.'
    if disruption_type in ['Technical', 'Weather']:
        from optimization import optimized_allocation_flow
        optimized_allocation_flow()
        return True, f'Disruption recorded and optimization triggered for {flight_no}.'

    return True, 'Disruption recorded.'


def notifications_page(message=None):
    path = 'rebooking_notifications.csv'
    if not Path(path).exists():
        content = '<p>No notifications generated yet.</p>'
    else:
        with open(path, encoding='utf-8') as f:
            lines = [line.strip().split(',') for line in f if line.strip()]
        rows = [[pid, name, fno, suggestions, status] for pid, name, fno, suggestions, status in lines]
        content = '<h2>Rebooking Notifications</h2>' + table_from_objects(['Passenger', 'Name', 'Original Flight', 'Suggested Flights', 'Status'], rows)
    return render_page('Rebooking Notifications', content, message)


def actions_page(params=None, message=None):
    content = (
        '<h2>System Actions</h2>'
        '<form method="post">'
        '<input type="hidden" name="action" value="cleanup">'
        '<button type="submit">Release Expired Allocations</button>'
        '</form>'
        '<form method="post">'
        '<input type="hidden" name="action" value="schedule_pending">'
        '<button type="submit">Allocate Pending Flights</button>'
        '</form>'
        '<form method="post">'
        '<input type="hidden" name="action" value="resolve_conflicts">'
        '<button type="submit">Resolve Resource Conflicts</button>'
        '</form>'
        '<form method="post">'
        '<input type="hidden" name="action" value="system_rebalance">'
        '<button type="submit">Run Emergency System Rebalance</button>'
        '</form>'
    )
    return render_page('System Actions', content, message)


def handle_action(params):
    action = params.get('action', '')
    if action == 'cleanup':
        release_expired_allocations()
        return True, 'Expired allocations released.'
    if action == 'schedule_pending':
        try_schedule_pending_flights()
        return True, 'Pending flights allocation attempted.'
    if action == 'resolve_conflicts':
        resolve_conflicts()
        return True, 'Conflict resolution completed.'
    if action == 'system_rebalance':
        system_rebalance()
        return True, 'Emergency system rebalance completed.'
    return False, 'Unknown action.'


def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    method = environ.get('REQUEST_METHOD', 'GET')
    params = {}
    message = None

    if method == 'POST':
        params = parse_post(environ)

    if path == '/':
        return response(start_response, home_page(message))

    if path == '/flights':
        if method == 'POST':
            if params.get('action') == 'add_flight':
                success, message = handle_add_flight(params)
            elif params.get('action') == 'allocate_flight':
                success, message = handle_allocate_flight(params)
            else:
                success, message = False, 'Unknown flight action.'
            return response(start_response, all_flights_page(params, message if success else f'Error: {message}'))
        return response(start_response, all_flights_page(params))

    if path == '/counters':
        if method == 'POST':
            success, message = handle_add_counter(params)
            return response(start_response, counters_page(params, message if success else f'Error: {message}'))
        return response(start_response, counters_page(params))

    if path == '/passengers':
        if method == 'POST':
            success, message = handle_book_passenger(params)
            return response(start_response, passengers_page(params, message if success else f'Error: {message}'))
        return response(start_response, passengers_page(params))

    if path == '/aircraft':
        if method == 'POST':
            success, message = handle_add_aircraft(params)
            return response(start_response, aircraft_page(params, message if success else f'Error: {message}'))
        return response(start_response, aircraft_page(params))

    if path == '/crew':
        if method == 'POST':
            success, message = handle_add_crew(params)
            return response(start_response, crew_page(params, message if success else f'Error: {message}'))
        return response(start_response, crew_page(params))

    if path == '/gates':
        if method == 'POST':
            success, message = handle_add_gate(params)
            return response(start_response, gates_page(params, message if success else f'Error: {message}'))
        return response(start_response, gates_page(params))

    if path == '/runways':
        if method == 'POST':
            success, message = handle_add_runway(params)
            return response(start_response, runways_page(params, message if success else f'Error: {message}'))
        return response(start_response, runways_page(params))

    if path == '/resources':
        if method == 'POST':
            success, message = handle_add_resource(params)
            return response(start_response, resources_page(params, message if success else f'Error: {message}'))
        return response(start_response, resources_page(params))

    if path == '/disruptions':
        if method == 'POST':
            success, message = handle_add_disruption(params)
            return response(start_response, disruptions_page(params, message if success else f'Error: {message}'))
        return response(start_response, disruptions_page(params))

    if path == '/notifications':
        return response(start_response, notifications_page(message))

    if path == '/actions':
        if method == 'POST':
            success, message = handle_action(params)
            return response(start_response, actions_page(params, message if success else f'Error: {message}'))
        return response(start_response, actions_page(params))

    start_response('404 Not Found', [('Content-type', 'text/plain; charset=utf-8')])
    return [b'Page not found']


if __name__ == '__main__':
    print('Starting Airport Operations web front end on http://127.0.0.1:8000')
    with make_server('127.0.0.1', 8000, application) as httpd:
        httpd.serve_forever()
