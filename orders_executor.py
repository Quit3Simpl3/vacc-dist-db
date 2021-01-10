from persistence.dto import Vaccine
from persistence.repository import repo


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
        self.amount = int(amount)
        self.date = date
        self.supplier = repo.suppliers.get(name=self.name)[0]
        self.logistic = repo.logistics.get(id=self.supplier.logistic)[0]

    def update_logistic(self):
        count_received = self.logistic.count_received + self.amount
        repo.logistics.update({"count_received": count_received}, {"id": self.logistic.id})

    def add_vaccine(self):
        vaccine = Vaccine(None, self.date, self.supplier.id, self.amount)
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
        self.clinic = repo.clinics.get(location=clinic)[0]
        self._amount = int(amount)
        self.logistic = repo.logistics.get(id=self.clinic.logistic)[0]

    @property
    def amount(self):
        return self._amount

    def acquire_vaccines(self):
        # get the required amount of vaccines from db
        tmp_amount = self.amount
        while tmp_amount > 0:
            vaccine = repo.vaccines.get_all(order_by="date", ascending=True)[0] # get the vaccines, oldest first
            if vaccine.quantity > tmp_amount:
                vaccine.quantity -= tmp_amount
                repo.vaccines.update({"quantity": vaccine.quantity}, {"id": vaccine.id})
                tmp_amount = 0

            else:
                tmp_amount -= vaccine.quantity
                repo.vaccines.delete(id=vaccine.id)  # update vaccine table

    def update_logistic(self):
        count_sent = self.logistic.count_sent + self.amount
        repo.logistics.update({"count_sent": count_sent}, {"id": self.logistic.id})

    def update_clinic(self):
        demand = self.clinic.demand - self.amount
        repo.clinics.update({"demand":demand}, {"id":self.clinic.id})

    def send(self):
        self.acquire_vaccines()
        self.update_logistic()
        self.update_clinic()

    def execute(self):
        self.send()
        super().execute()
