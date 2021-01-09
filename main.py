from sys import argv

from persistence.repository import repo # creates the db when importing repo
from output_writer import OutputWriter
from orders_executor import SendOrder, ReceiveOrder

def main():
    parse_config_file(argv[1]) # read & parse config.txt and configure the db
    execute_orders(argv[2], argv[3]) # read line-by-line & parse orders.txt and execute the orders. create output.txt

def execute_orders(orders_path, output_path):
    output_writer = OutputWriter(output_path)
    with open(path, "rb") as file:
        lines = file.readlines()
        for line in lines:
            args = line.split(",")
            order = None
            if len(args) == 3: # Receive order
                order = ReceiveOrder(args[0], args[1], args[2], output_writer)

            elif len(args) == 2: # Send order
                order = SendOrder(args[0], args[1], output_writer)

            if order:
                order.execute()

            else:
                print("ERROR")


def parse_config_file(path):
    with open(path) as file:
        lines = file.readlines()
        a = lines[0]
        lines_count = a.split(",") # Get how many lines for each table
        vaccines_count = lines_count[0]
        suppliers_count = lines_count[1]
        clinics_count = lines_count[2]
        logistics_count = lines_count[3]
        lines = lines[1:] # Skip the first line

        # Bulk insert all the DTOs into the DB:
        repo.vaccines.insert_bulk([Vaccine(*line.split(",")) for line in lines[:vaccines_count]])
        repo.suppliers.insert_bulk([Supplier(*line.split(",")) for line in lines[:suppliers_count]])
        repo.clinics.insert_bulk([Clinic(*line.split(",")) for line in lines[:clinics_count]])
        repo.logistics.insert_bulk([Logistic(*line.split(",")) for line in lines[:logistics_count]])

if __name__ == "__main__":
    main()