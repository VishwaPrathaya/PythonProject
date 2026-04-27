from validation import validate_resource


class Resource:

    def __init__(self, res_id, res_type, status):
        self.res_id = res_id
        self.res_type = res_type
        self.status = status


# ---------------- LOAD ----------------
def load_resources():

    resource_list = []

    try:
        with open("ground_resources.csv", "r") as f:
            for line in f:
                data = line.strip().split(",")

                if len(data) != 3:
                    continue

                resource_list.append(Resource(*data))

    except FileNotFoundError:
        pass

    return resource_list


# ---------------- DISPLAY ----------------
def display_resources():

    resource_list = load_resources()

    if not resource_list:
        print("\nNo ground resources available.")
        return

    print("\n===== GROUND RESOURCES =====")

    for r in resource_list:
        print("\nResource ID   :", r.res_id)
        print("Type          :", r.res_type)
        print("Status        :", r.status)
        print("-----------------------------")


# ---------------- WRITE ----------------
def writeData():

    print("Ground Resources Module")

    n = int(input("Enter number of resources: "))
    existing = load_resources()

    new_added = False

    with open("ground_resources.csv", "a") as file:

        for i in range(n):

            print("\nResource", i + 1)

            res_id = input("Resource ID: ")
            res_type = input("Resource Type: ")
            status = input("Status (Available/In Use): ")

            if not validate_resource(res_id, res_type, status):
                print("Invalid input. Skipping...\n")
                continue

            if any(r.res_id == res_id for r in existing):
                print("Duplicate Resource ID not allowed")
                continue

            file.write(",".join([res_id, res_type, status]) + "\n")

            existing.append(Resource(res_id, res_type, status))
            new_added = True

    print("\n✅ Resources added successfully!")

    # 🔥 TRIGGER (same as aircraft)
    if new_added:
        print("🔄 New resources available → reallocating flights")
        from allocation_engine import try_schedule_pending_flights
        try_schedule_pending_flights()


# ---------------- REMOVE ----------------
def remove_resource():

    rid = input("Enter Resource ID to remove: ")

    resources = load_resources()
    updated = []

    found = False

    from allocation_engine import load_allocations
    allocations = load_allocations()

    for r in resources:

        if r.res_id == rid:
            found = True

            # 🔥 If resource used → remove full allocation
            for fno, data in allocations.items():

                if len(data) > 5:
                    used_resources = data[5].split("|")

                    if rid in used_resources:
                        print(f"⚠️ Resource used by flight {fno} → removing allocation")

                        from allocation_engine import remove_allocation_for_flight
                        remove_allocation_for_flight(fno)

            continue

        updated.append(r)

    if not found:
        print("❌ Resource not found")
        return

    # 🔹 SAVE FILE
    with open("ground_resources.csv", "w") as f:
        for r in updated:
            f.write(",".join([
                r.res_id, r.res_type, r.status
            ]) + "\n")

    print("✅ Resource removed successfully")

    # 🔥 TRIGGER
    print("🔄 Reallocating pending flights...")
    from allocation_engine import try_schedule_pending_flights
    try_schedule_pending_flights()


# ---------------- UPDATE ----------------
def update_resource():

    resources = load_resources()

    if not resources:
        print("No resources available")
        return

    rid = input("Enter Resource ID to update: ")

    target = next((r for r in resources if r.res_id == rid), None)

    if not target:
        print("Resource not found")
        return

    print(f"\nCurrent: {target.res_id} | {target.res_type} | {target.status}")
    print("Leave blank to keep current value\n")

    rtype = input(f"Type [{target.res_type}]: ").strip()
    status = input(f"Status [{target.status}]: ").strip()

    old_status = target.status

    # 🔹 APPLY CHANGES
    if rtype:
        target.res_type = rtype

    if status:
        if status not in ["Available", "In Use"]:
            print("Invalid status")
            return
        target.status = status

    # 🔹 SAVE FILE
    with open("ground_resources.csv", "w") as f:
        for r in resources:
            f.write(",".join([
                r.res_id,
                r.res_type,
                r.status
            ]) + "\n")

    print(f"✅ Resource {rid} updated successfully")

    # 🔥 SMART TRIGGER (same as aircraft)

    # ✅ Became AVAILABLE → allocate
    if target.status == "Available" and old_status != "Available":
        print("🔄 Resource became available → reallocating flights")

        from allocation_engine import try_schedule_pending_flights
        try_schedule_pending_flights()

    # ⚠️ Became IN USE manually → reset system
    elif target.status == "In Use" and old_status == "Available":
        print("⚠️ Resource manually occupied → resetting allocations")

        from allocation_engine import load_allocations, remove_allocation_for_flight

        allocations = load_allocations()

        for fno, data in allocations.items():

            if len(data) > 5:
                used_resources = data[5].split("|")

                if rid in used_resources:
                    remove_allocation_for_flight(fno)

        from allocation_engine import try_schedule_pending_flights
        try_schedule_pending_flights()