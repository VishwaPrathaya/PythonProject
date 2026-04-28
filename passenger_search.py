def search_flights(flights, origin=None, destination=None, time_from=None, time_to=None):

    results = []

    for f in flights:

        if origin and f.origin != origin:
            continue

        if destination and f.destination != destination:
            continue

        # - Time range filter (ONLY if provided)
        if time_from is not None and time_to is not None:
            if not (time_from <= int(f.arr) <= time_to or
                    time_from <= int(f.dep) <= time_to):
                continue

        results.append(f)

    return results