class OutputWriter():
    def __init__(self, path):
        self.path = path

    def get_total_inventory(self):
        vaccine_quantities = repo.vaccines.get_all(columns=["quantity"])
        return sum(vaccine_quantities)

    def get_total_demand(self):
        clinic_demands = repo.clinics.get_all(columns=["demand"])
        return sum(clinic_demands)

    def get_total_received(self):
        logistic_demands = repo.logistics.get_all(columns=["count_received"])
        return sum(logistic_demands)

    def get_total_sent(self):
        logistic_demands = repo.logistics.get_all(columns=["count_sent"])
        return sum(logistic_demands)

    def write(self):
        with open(self.path, "wb") as file:
            file.writeline("{inventory},{demand},{received},{sent}".format(
                inventory=self.get_total_inventory(),
                demand=self.get_total_demand(),
                received=self.get_total_received(),
                sent=self.get_total_sent()
                ))