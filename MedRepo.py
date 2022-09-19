from database.MedDatabase import MedDatabase
from database.entities.Entity import Patients, Question


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class MedRepo(Singleton):
    def __init__(self):
        self.db = MedDatabase()

    def add_patient(self, patient: Patients):
        self.db.add_patient(patient.name, patient.age, patient.male)

    def get_count_questions(self) -> int:
        return self.db.get_count_questions()


    def insert_question(self, question: Question):
        self.db.insert_question(question)

