from collections import defaultdict

from allocation_engine import load_allocations, remove_allocation_for_flight, try_schedule_pending_flights
from flights import load_flights
from optimization import flight_priority


def _times_overlap(arrival_a, departure_a, arrival_b, departure_b):
    return not (departure_a <= arrival_b or departure_b <= arrival_a)


def _normalize_resource_id(resource_id):
    if resource_id is None:
        return None
    return str(resource_id).strip()


def detect_conflicts():
    flights = load_flights()
    allocations = load_allocations()

    if not allocations:
        print("No allocations available to inspect.")
        return []

    flight_map = {f.fno: f for f in flights}
    resource_map = defaultdict(list)

    for fno, data in allocations.items():
        flight = flight_map.get(fno)
        if not flight:
            continue

        try:
            arr = int(flight.arr)
            dep = int(flight.dep)
        except Exception:
            continue

        if len(data) >= 4:
            gate_id = _normalize_resource_id(data[2])
            runway_id = _normalize_resource_id(data[3])
            if gate_id and gate_id != "NA":
                resource_map[("Gate", gate_id)].append((flight, arr, dep))
            if runway_id and runway_id != "NA":
                resource_map[("Runway", runway_id)].append((flight, arr, dep))

        if len(data) >= 5:
            crew_ids = [c for c in data[4].split("|") if c and c != "NA"]
            for crew_id in crew_ids:
                resource_map[("Crew", crew_id)].append((flight, arr, dep))

        if len(data) >= 6:
            resource_ids = [r for r in data[5].split("|") if r and r != "NA"]
            for res_id in resource_ids:
                resource_map[("GroundResource", res_id)].append((flight, arr, dep))

        if len(data) >= 7:
            counter_ids = [c for c in data[6].split("|") if c and c != "NA"]
            for counter_id in counter_ids:
                resource_map[("Counter", counter_id)].append((flight, arr, dep))

    conflicts = []

    for (resource_type, resource_id), records in resource_map.items():
        if len(records) < 2:
            continue

        for i in range(len(records)):
            for j in range(i + 1, len(records)):
                flight_a, arr_a, dep_a = records[i]
                flight_b, arr_b, dep_b = records[j]

                if _times_overlap(arr_a, dep_a, arr_b, dep_b):
                    conflicts.append({
                        "resource_type": resource_type,
                        "resource_id": resource_id,
                        "flight_a": flight_a.fno,
                        "flight_b": flight_b.fno,
                        "flight_a_arr": arr_a,
                        "flight_a_dep": dep_a,
                        "flight_b_arr": arr_b,
                        "flight_b_dep": dep_b,
                    })

    if not conflicts:
        print("No resource conflicts detected.")
    else:
        print(f"Detected {len(conflicts)} conflict(s):")
        for conflict in conflicts:
            print(
                f" - {conflict['resource_type']} {conflict['resource_id']} conflict: "
                f"Flight {conflict['flight_a']} ({conflict['flight_a_arr']}-{conflict['flight_a_dep']}) vs "
                f"Flight {conflict['flight_b']} ({conflict['flight_b_arr']}-{conflict['flight_b_dep']})"
            )

    return conflicts


def resolve_conflicts():
    print("\n=== CONFLICT RESOLUTION STARTED ===")
    conflicts = detect_conflicts()

    if not conflicts:
        print("Conflict resolution complete: no action required.")
        return

    flights = load_flights()
    flight_map = {f.fno: f for f in flights}
    flights_to_release = set()

    for conflict in conflicts:
        flight_a = flight_map.get(conflict["flight_a"])
        flight_b = flight_map.get(conflict["flight_b"])

        if not flight_a or not flight_b:
            continue

        ordered = sorted([flight_a, flight_b], key=flight_priority, reverse=True)
        keep = ordered[0]
        release = ordered[1]

        flights_to_release.add(release.fno)
        print(
            f" Resolving conflict on {conflict['resource_type']} {conflict['resource_id']}: "
            f"keeping {keep.fno}, releasing {release.fno}"
        )

    if not flights_to_release:
        print("No conflicting allocations could be resolved.")
        return

    for fno in sorted(flights_to_release):
        print(f" Releasing allocation for flight {fno}")
        remove_allocation_for_flight(fno, auto_reallocate=False)

    print(" Attempting to reallocate pending flights after conflict resolution...")
    try_schedule_pending_flights()
    print("=== CONFLICT RESOLUTION COMPLETE ===\n")
