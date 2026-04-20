from data_loader import load_flights

class Passenger:

    def __init__(self, pid, name, fno, seat, ticket_class="Economy", status="Booked"):
        self.pid = pid
        self.name = name
        self.fno = fno
        self.seat = seat
        self.ticket_class = ticket_class
        self.status = status


# ---------------- LOAD ----------------
def load_passengers():

    lst = []

    try:
        with open("passenger.txt") as f:
            for line in f:
                data = line.strip().split(",")

                if len(data) not in [4, 6]:
                    continue

                lst.append(Passenger(*data))
    except FileNotFoundError:
        pass

    return lst


# ---------------- DISPLAY ----------------
def display_passengers():

    passengers = load_passengers()

    if not passengers:
        print("No passengers found")
        return

    print("\n--- PASSENGERS ---")
    for p in passengers:
        print(f"{p.pid} | {p.name} | {p.fno} | {p.seat}")


# ---------------- SEAT COUNT ----------------
def seats_used(fno):

    return sum(1 for p in load_passengers() if p.fno == fno)