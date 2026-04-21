from validation import validate_resource
from constraint_checking import check_resource_constraints


class Resource:

    def __init__(self, res_id, res_type, status):

        self.res_id = res_id
        self.res_type = res_type
        self.status = status


def load_resources():

    resource_list = []

    try:
        with open("ground_resources.txt", "r") as f:
            for line in f:

                data = line.strip().split(",")

                if len(data) != 3:
                    print("Invalid resource data:", line)
                    continue

                resource_list.append(Resource(*data))

    except FileNotFoundError:
        print("ground_resources.txt not found.")

    return resource_list

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

def writeData():

    print("Ground Resources Module")

    n = int(input("Enter number of resources: "))
    existing = load_resources()  

    with open("ground_resources.txt", "a") as file:

        for i in range(n):

            print("\nResource", i + 1)

            res_id = input("Resource ID: ")
            res_type = input("Resource Type: ")
            status = input("Status (Available/In Use): ")

            if not validate_resource(res_id, res_type, status):
                print("Invalid input. Skipping...\n")
                continue

            # 🔹 Duplicate check
            if any(r.res_id == res_id for r in existing):
                print("Duplicate Resource ID not allowed")
                continue

            file.write(",".join([res_id, res_type, status]) + "\n")

            # update list
            existing.append(Resource(res_id, res_type, status))

    print("\nResources added successfully!")
    