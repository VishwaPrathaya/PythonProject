from allocation_engine import allocate_flight
from flights import load_flights


# ---------------- PRIORITY RULE ----------------
def flight_priority(f):

    score = 0

    # International flights → higher priority
    if f.flight_type == "International":
        score += 100

    # Earlier arrival → higher priority
    try:
        score += (1000 - int(f.arr))
    except:
        pass

    return score


# ---------------- SORT FLIGHTS ----------------
def prioritize_flights(flights):
    return sorted(flights, key=flight_priority, reverse=True)


# ---------------- MAIN OPTIMIZATION ENGINE ----------------
def optimized_allocation_flow():

    flights = load_flights()

    if not flights:
        print("No flights available for optimization")
        return

    # Step 1: sort flights
    ordered_flights = prioritize_flights(flights)

    print("\n=== OPTIMIZED ALLOCATION STARTED ===")

    allocated = 0
    skipped = 0

    # Step 2: allocate each flight
    for f in ordered_flights:

        # skip already allocated flights
        if getattr(f, "aircraft", "NA") != "NA":
            skipped += 1
            continue

        print(f"\n Allocating Flight {f.fno}...")
        allocate_flight(f)

        from allocation_engine import load_allocations

        allocations = load_allocations()

        if f.fno in allocations:
             allocated += 1

    print("\n=== OPTIMIZATION COMPLETE ===")
    print(f" Allocated: {allocated}")
    #print(f"⏭ Skipped (already allocated): {skipped}")