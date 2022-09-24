from typing import Optional

from database.MedDatabase import MedDatabase
from database.entities.Entity import Patients, Question, Answer


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

    def get_questions(self) -> list[Question]:
        return self.db.get_questions_order()

    def insert_question(self, question: Question):
        self.db.insert_question(question)

    def get_enable_answers(self, question_id: int) -> list[Answer]:
        return self.db.get_enable_answers(question_id)

    def update_question(self, question: Question):
        self.db.update_question(question)

    def get_question_id_by_name(self, name: str) -> Optional[int]:
        return self.db.get_question_id_by_name(name)

    def delete_question(self, question_id: int):
        self.db.delete_question(question_id)

    def get_question_witch_more_than_order(self, order: int) -> list[Question]:
        return self.db.get_question_witch_more_than_order(order)

    def update_jump(self, question_id: int, answer_id: int, destination_id: int):
        self.db.update_jump(question_id, answer_id, destination_id)
