from persistence.dto import Vaccine

class Order():
    def __init__(self, output_writer):
        self.output_writer = output_writer

    def write_output(self):
        self.output_writer.write()

    def execute(self):
        self.write_output()

    class Meta:
        abstract = True


class ReceiveOrder(Order):
    def __init__(self, name, amount, date, output_writer):
        super().__init__(output_writer)
        self.name = name
        self.amount = amount
        self.date = date
        self.supplier = repo.suppliers.get({"name": self.name})
        self.logistic = repo.logistics.get({"id": self.supplier.logistic})

    def update_logistic(self):
        count_received = self.logistic.count_received + self.amount
        repo.logistics.update({"count_received": count_received}, {"id": self.logistic.id})

    def add_vaccine(self):
        vaccine = Vaccine(self.name, self.date, self.supplier.id, self.amount)
        repo.vaccines.insert(vaccine)

    def receive(self):
        self.add_vaccine()
        self.update_logistic()

    def execute(self):
        self.receive()
        super().execute()


class SendOrder(Order):
    def __init__(self, clinic, amount, output_writer):
        super().__init__(output_writer)
        self.clinic = clinic
        self.amount = amount
        self.logistic = repo.logistics.get({"id": self.clinic.logistic})

    def acquire_vaccines(self):
        # get the required amount of vaccines from db
        vaccines = []
        tmp_amount = self.amount
        while tmp_amount > 0:
            vaccine = repo.vaccines.get(order_by="date")
            if vaccine.quantity > self.amount:
                vaccine.quantity -= tmp_amount
                repo.vaccines.update({"quantity": vaccine.quantity}, {"id": vaccine.id})
                tmp_amount = 0
            else:
                tmp_amount -= vaccine.quantity
                repo.vaccines.delete({"id": vaccine.id}) # update vaccine table

    def update_logistic(self):
        count_sent = self.logistic.count_sent + self.amount
        repo.logistics.update({"count_sent": count_sent}, {"id": self.logistic.id})

    def update_clinic(self):
        demand = self.clinic.demand - self.amount
        repo.clinics.update({"demand": demand}, {"id": self.clinic.id})

    def send(self):
        self.acquire_vaccines()
        self.update_logistic()
        self.update_clinic()

    def execute(self):
        self.receive()
        super().execute()