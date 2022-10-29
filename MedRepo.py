from collections import deque
from typing import Optional, List, Dict, Union

from database.MedDatabase import MedDatabase
from database.entities.Entity import Patient, Question, Answer, EnableAnswers


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class MedRepo(Singleton):
    def __init__(self):
        self._db = MedDatabase()

    def add_patient(self, patient: Patient):
        self._db.add_patient(patient.name, patient.age, patient.male)

    def get_question_by_id(self, id_: int) -> Question:
        return self._db.get_question_by_id(id_)

    def get_count_questions(self) -> int:
        return self._db.get_count_questions()

    def get_questions(self) -> list[Question]:
        return self._db.get_questions_order()

    def insert_question(self, question: Question):
        self._db.insert_question(question)

    def get_enable_answers(self, question_id: int) -> list[Answer]:
        return self._db.get_enable_answers(question_id)

    def update_question(self, question: Question):
        self._db.update_question(question)

    def get_question_id_by_name(self, name: str) -> Optional[int]:
        return self._db.get_question_id_by_name(name)

    def delete_question(self, question_id: int):
        self._db.delete_question(question_id)

    def get_last_question_in_block(self, block: int) -> Question:
        return self._db.get_last_question(block)

    def get_first_question_in_block(self, block: int) -> Question:
        return self._db.get_first_question(block)

    def get_next_questions(self, question_id: int) -> list[Question]:
        return self._db.get_next_questions(question_id)

    def get_jump(self, question_id: int) -> dict[Union[str, Answer], list[bool, list[Question]]]:
        return self._db.get_jump(question_id)

    def update_jump(self, question_id: int, answer_id: int, destination_id: int):
        self._db.update_jump(question_id, answer_id, destination_id)

    def update_cycle(self, question_id: int, answer_id: int, start_id: int, finish_id: int, cycle: int):
        self._db.update_cycle(question_id, answer_id, start_id, finish_id, cycle)

    def get_patients_name(self) -> list[Patient]:
        return self._db.get_patients()

    def delete_patient(self, patient_id):
        self._db.delete_patient(patient_id)

    def add_answer_to_question(self, answer: str, question_id: int) -> int:
        return self._db.add_answer_to_question(answer, question_id)

    def delete_question_with_answer(self, question_id: int, answer_id: int):
        self._db.delete_question_with_answer(question_id, answer_id)

    def delete_branch(self, question: Question, answer_id: int):
        self._db.delete_branch(question, answer_id)

    def update_next_question(self, old_question_id: int, new_question_id: int):
        # это первый вопрос
        if old_question_id <= -1:
            self._db.set_start_question(new_question_id)
        # это не первый вопрос
        else:
            self._db.update_next_question(old_question_id, new_question_id)

    def set_prev_question(self, prev_question_id: int, current_question: Question):
        self._db.set_prev_question(prev_question_id, current_question)

    def get_deque_enable_answers(self) -> list[EnableAnswers]:
        return self._db.get_deque_enable_answers()
