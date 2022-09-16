from database.MedDatabase import MedDatabase
from database.entities.Entity import Patients


class MedRepo:
    def __init__(self):
        self.db = MedDatabase()

    def add_patient(self, patient: Patients):
        self.db.add_patient(patient.name, patient.age, patient.male)
