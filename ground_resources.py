from validation import validate_resource
from constraint_checking import check_resource_constraints


class Resource:

    def __init__(self, res_id, res_type, status):

        self.res_id = res_id
        self.res_type = res_type
        self.status = status

    def display(self):
        print("Resource ID:", self.res_id,
              "| Type:", self.res_type,
              "| Status:", self.status)


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
        print("\nNo resources available.")
        return

    print("\n--- Ground Resources ---")

    for r in resource_list:
        r.display()


def writeData():

    print("Ground Resources Module")

    n = int(input("Enter number of resources: "))

    with open("ground_resources.txt", "a") as file:

        for i in range(n):

            print("\nResource", i + 1)

            res_id = input("Resource ID: ")
            res_type = input("Resource Type: ")
            status = input("Status (Available/In Use): ")

            # VALIDATION
            if not validate_resource(res_id, res_type, status):
                print("Invalid input. Skipping...\n")
                continue

            resource_list = load_resources()

            # CONSTRAINT CHECK
            if not check_resource_constraints(resource_list, res_id):
                print("Constraint violation. Skipping...\n")
                continue

            file.write(",".join([res_id, res_type, status]) + "\n")

    print("\nResources added successfully!")
    display_resources()
    