from validation import validate_gate


class Gate:

    def __init__(self, gid, terminal, gtype, size, availability):
        self.gate_id = gid
        self.terminal = terminal
        self.gate_type = gtype
        self.max_aircraft_size = size
        self.availability = availability


# ---------------- LOAD ----------------
def load_gates():
    lst = []

    try:
        with open("gates.txt") as f:
            for line in f:
                data = line.strip().split(",")

                if len(data) != 5:
                    continue

                lst.append(Gate(*data))
    except:
        pass

    return lst


# ---------------- DISPLAY ----------------
def display_gates():

    gates = load_gates()

    if not gates:
        print("No gates available")
        return

    print("\n--- Gates ---")
    for g in gates:
        print(f"{g.gate_id} | {g.terminal} | {g.gate_type} | {g.max_aircraft_size} | {g.availability}")


# ---------------- WRITE ----------------
def writeData():

    n = int(input("Number of gates: "))
    existing = load_gates()

    new_gates_added = False

    with open("gates.txt", "a") as f:

        for _ in range(n):

            gid = input("Gate ID: ")
            terminal = input("Terminal: ")
            gtype = input("Type (Domestic/International): ")
            size = input("Max Size (Wide/Narrow): ")
            availability = "Free"   # 🔥 IMPORTANT FIX (don’t take input)

            if not validate_gate(gid, gtype, size, availability):
                continue

            if any(g.gate_id == gid for g in existing):
                print("Duplicate Gate ID")
                continue

            f.write(",".join([gid, terminal, gtype, size, availability]) + "\n")

            existing.append(Gate(gid, terminal, gtype, size, availability))
            new_gates_added = True

    print("✅ Gates added")
     
    from allocation_engine import auto_allocate_gate
    auto_allocate_gate()

