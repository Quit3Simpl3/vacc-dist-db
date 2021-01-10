from sys import argv

from persistence.dto import Vaccine, Supplier, Clinic, Logistic
from persistence.repository import repo  # creates the db when importing repo
from output_writer import OutputWriter
from orders_executor import SendOrder, ReceiveOrder
from file_reader import FilerReader


def main(argv):
    parse_config_file(argv[1])  # read & parse config.txt and configure the db
    execute_orders(argv[2], argv[3])  # read line-by-line & parse orders.txt and execute the orders. create output.txt


def execute_orders(orders_path, output_path):
    output_writer = OutputWriter(output_path)
    reader = FilerReader(orders_path)
    while reader.has_next_line():
        args = reader.next_line().split(",")
        order = None
        if len(args) == 3:  # Receive order
            order = ReceiveOrder(args[0], args[1], args[2], output_writer)

        elif len(args) == 2:  # Send order
            order = SendOrder(args[0], args[1], output_writer)

        if order:
            order.execute()

        else:
            print("ERROR")


def parse_config_file(path):
    reader = FilerReader(path)
    lines = reader.readlines()
    lines_count = lines[0].split(",")  # Get how many lines for each table
    vaccines_index = int(lines_count[0])
    suppliers_index = int(lines_count[1]) + vaccines_index
    clinics_index = int(lines_count[2]) + suppliers_index
    logistics_index = int(lines_count[3]) + clinics_index
    lines = lines[1:]  # Skip the first line

    # Bulk insert all the DTOs into the DB:
    repo.vaccines.insert_bulk([Vaccine(*line.split(",")) for line in lines[:vaccines_index]])
    repo.suppliers.insert_bulk([Supplier(*line.split(",")) for line in lines[vaccines_index:suppliers_index]])
    repo.clinics.insert_bulk([Clinic(*line.split(",")) for line in lines[suppliers_index:clinics_index]])
    repo.logistics.insert_bulk([Logistic(*line.split(",")) for line in lines[clinics_index:logistics_index]])


if __name__ == "__main__":
    main(argv)
