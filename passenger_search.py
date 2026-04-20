def search_flights(flights, origin=None, destination=None, time=None):

    results = []

    for f in flights:

        if origin and f.origin != origin:
            continue

        if destination and f.destination != destination:
            continue

        if time:
            if f.arr != time and f.dep != time:
                continue

        results.append(f)

    return results