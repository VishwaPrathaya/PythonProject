# PythonProject — README

## Counter Module

Purpose
- Manage check-in / boarding counters and integrate them into the allocation engine.

CSV format (`counters.csv`)
- `counter_id` — unique counter identifier (e.g. `G1-CNT1`)
- `gate_id` — gate the counter belongs to (e.g. `G1`)
- `terminal` — terminal name (e.g. `T1`)
- `service_type` — one of `Check-In` or `Boarding`
- `availability` — `Available` or `Occupied`
- `capacity` (optional) — integer passenger capacity; default is 50 when missing

Each row example:

G1-CNT1,G1,T1,Check-In,Available,50

Programmatic API (module `counters`)
- `load_counters()` → returns list of `Counter` objects
- `get_available_counters(gate_id, counters)` → filter counters for a gate and availability
- `add_counter()` → interactive CLI helper to append counters
- `create_counter(counter_id, gate_id, terminal, service_type, availability, capacity=50)` → programmatic creation and append to `counters.csv`
- `update_counter_file(counters)` → overwrite `counters.csv` from list

Integration notes
- The allocation engine (`allocation_engine.py`) will select one or more counters for a flight by capacity. When existing counters cannot meet demand, it will auto-create counters via `create_counter()` and re-run selection.
- Allocations persist selected counters in `flight_allocations.csv` as a pipe-separated list in the counters column (e.g. `G1-CNT1|G1-CNT2`).
- `passenger_allocation.allocate_passengers()` propagates the flight's allocated counters into each passenger's `counter_id` field in `passenger.csv`.

Usage
- CLI: run `main.py` and use the `Counters` menu to view/add/update counters.
- Programmatic: import `counters` and use `create_counter(...)` to add counters from scripts or tests.

Testing
- Automated smoke tests covering counter auto-creation and passenger assignment are in `tests/smoke_tests.py`.

Web Front End
- A minimal web front end is provided in `frontend.py`.
- Start the app with:

```bash
python frontend.py
```

- Open `http://127.0.0.1:8000` in your browser to manage flights, passengers, counters, disruptions, and actions.

Contact
- See project files for more modules and integration points.
