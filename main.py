from sys import argv
from persistence.repository import repo # creates the db when importing repo

def main():
    #> python3 main.py config.txt orders.txt output.txt
    parse_config_file(argv[1]) # read & parse config.txt and configure the db
    orders_path = argv[2] # read line-by-line & parse orders.txt and execute the orders
    output_path = argv[3] # create output.txt according to the supplied path

def parse_config_file(path):
    with open(path, "rb") as file:
        lines = file.readlines()
        lines_count = lines[0].split(",") # Get how many lines for each table
        vaccines_count = lines_count[0]
        suppliers_count = lines_count[1]
        clinics_count = lines_count[2]
        logistics_count = lines_count[3]
        lines = lines[1:] # Skip the first line

        # Bulk insert all the DTOs into the DB:
        repo.vaccines.insert_bulk([Vaccine(*lines.split(",")) for line.split(",") in lines[:vaccines_count]])
        repo.suppliers.insert_bulk([Supplier(*lines.split(",")) for line.split(",") in lines[:suppliers_count]])
        repo.clinics.insert_bulk([Clinic(*lines.split(",")) for line.split(",") in lines[:clinics_count]])
        repo.logistics.insert_bulk([Logistic(*lines.split(",")) for line.split(",") in lines[:logistics_count]])

if __name__ == "__main__":
    pass # TODO