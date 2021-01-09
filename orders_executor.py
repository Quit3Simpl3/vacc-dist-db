class Orders():
    def __init__(self):
        self.clinic_dao = Dao(dto.Clinic, self.conn)

    def receive(self, supplier_name, amount, date):
        pass # TODO: insert to the db the shipment

    def send(self, clinic_name, amount):
        pass # TODO: insert to the db the shipment
        clinic = repo.get_clinic(clinic_name) # Clinic DTO
        ...
        # Option 1:
        repo.update_clinic(amount=clinic.amount+amount) # -> repo.dao.update(Clinic,...
        # Option 2:
        self.clinic_dao.update(clinic, {"amount", })



get_clinic(name):
    self.clinic = clinic_dao.get({"name", name})