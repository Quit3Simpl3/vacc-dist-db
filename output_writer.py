from persistence.repository import repo

class OutputWriter():
    def __init__(self, path):
        self.path = path
        with open(path, 'w'):
            pass

    def get_total_inventory(self):
        vaccines = repo.vaccines.get_all()
        return sum([vaccine.quantity for vaccine in vaccines])

    def get_total_demand(self):
        clinics = repo.clinics.get_all()
        return sum([clinic.demand for clinic in clinics])

    def get_total_received(self):
        logistics = repo.logistics.get_all()
        return sum([logistic.count_received for logistic in logistics])

    def get_total_sent(self):
        logistics = repo.logistics.get_all()
        return sum([logistic.count_sent for logistic in logistics])

    def write(self):
        with open(self.path, "a+") as file:
            file.write("{inventory},{demand},{received},{sent}\n".format(
                inventory=self.get_total_inventory(),
                demand=self.get_total_demand(),
                received=self.get_total_received(),
                sent=self.get_total_sent()
                ))
