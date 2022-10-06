import sqlite3
from typing import Optional

from database.entities.Entity import *


def _list_question_from_response(questions_list_response: list) -> list[Question]:
    return list(map(lambda question: Question(id_=question[0],
                                              name=question[1],
                                              short=question[2],
                                              type_=question[3],
                                              require=question[4],
                                              measure=question[5],
                                              private=question[6],
                                              order=question[7],
                                              ),
                    questions_list_response))


def _list_patients_from_response(patients_list_response: list) -> list[Patient]:
    return list(map(lambda patient: Patient(id_=patient[0],
                                            name=patient[1],
                                            male=patient[2],
                                            age=patient[3],
                                            ),
                    patients_list_response))


class MedDatabase:
    NAME_DB: str = "./med.db"

    def __init__(self):
        self.create_db()

    def execute(self, script: str, *args, need_answer: bool = False) -> Optional[list]:
        conn = sqlite3.connect(self.NAME_DB)
        cursor = conn.cursor()

        def close():
            conn.commit()
            cursor.close()
            conn.close()

        if args:
            cursor.execute(script, args)
        else:
            cursor.execute(script)

        if need_answer:
            answer: Optional[list] = cursor.fetchall()
            close()
            return answer
        else:
            close()

    def create_db(self):
        self.execute(Patient.CREATE_TABLE)
        self.execute(Answer.CREATE_TABLE)
        self.execute(PatientAnswer.CREATE_TABLE)
        self.execute(Question.CREATE_TABLE)
        self.execute(EnableAnswers.CREATE_TABLE)
        self.execute(RepeatQuestions.CREATE_TABLE)
        self.execute(QuestionType.CREATE_TABLE)

        # добавляем ответы Да и Нет с нужными id, если их еще нет в БД
        if not self.execute(Answer.GET_BOOL_ANSWERS, need_answer=True):
            self.execute(Answer.INSERT_BOOL_ANSWER)

        if not self.execute(QuestionType.GET_TYPES, need_answer=True):
            self.execute(QuestionType.INSERT_TYPES)

    def add_patient(self, name: str, age: int, male: int):
        self.execute(Patient.INSERT_ALL, name, age, male)

    def get_count_questions(self) -> int:
        return self.execute(Question.GET_COUNT, need_answer=True)[0][0] + 1

    def _get_id(self, check_query: str, check_field) -> Optional[int]:
        try:
            return self.execute(check_query, check_field, need_answer=True)[0][0]
        except IndexError:
            return None

    def _insert_entity_if_not_exist(self, check_query: str, check_field, insert_query: str, *insert_fields) -> int:
        id_ = self._get_id(check_query, check_field)
        if id_ is None:
            self.execute(insert_query, *insert_fields)
            id_ = self._get_id(check_query, check_field)
        return id_

    def insert_question(self, question: Question):
        question_id = self._insert_entity_if_not_exist(Question.GET_ID_BY_NAME, question.name,
                                                       Question.INSERT,
                                                       question.name, question.short, question.type_, question.measure,
                                                       question.require_int, question.private_int, question.order)
        if question.type_ == Question.TypeAnswer.BOOL.value:
            self.execute(EnableAnswers.INSERT_NO_ANSWER, question_id)
            self.execute(EnableAnswers.INSERT_YES_ANSWER, question_id)
        else:
            if question.type_ == Question.TypeAnswer.MANY.value and question.list_answers:
                for answer in question.list_answers:
                    answer_id = self._insert_entity_if_not_exist(Answer.GET_ID_BY_TEXT, answer, Answer.INSERT_INTO,
                                                                 answer)
                    self.execute(EnableAnswers.INSERT_ANSWER, question_id, answer_id)

    def get_question_id_by_name(self, name: str) -> Optional[int]:
        id_ = self._get_id(Question.GET_ID_BY_NAME, name)
        return id_

    def get_questions_order(self):
        questions_list = self.execute(Question.SELECT_ALL_ORDER_ASC, need_answer=True)
        return _list_question_from_response(questions_list)

    def get_enable_answers(self, question_id: int) -> list[Answer]:
        answers_list = self.execute(EnableAnswers.SELECT_BY_QUESTION_ID, question_id, need_answer=True)
        return list(map(lambda answer: Answer(id_=answer[0],
                                              name=answer[1],
                                              ),
                        answers_list))

    def update_question(self, question: Question):
        self.execute(Question.UPDATE_QUESTION,
                     question.name,
                     question.short,
                     question.type_,
                     question.measure,
                     question.require_int,
                     question.private_int,
                     question.id_,
                     )
        if question.list_answers:
            self.execute(EnableAnswers.DELETE_ANSWERS_FROM_QUESTION, question.id_)
            for answer in question.list_answers:
                answer_id = self.execute(Answer.GET_ID_BY_TEXT, answer)
                self.execute(EnableAnswers.INSERT_ANSWER, question.id_, answer_id)

    def delete_question(self, question_id: int):
        order = self.execute(Question.SELECT_ORDER_BY_ID, question_id, need_answer=True)[0][0]
        self.execute(Question.DELETE_BY_ID, question_id)
        self.execute(Question.UPDATE_ORDER, order)
        self.execute(EnableAnswers.DELETE_ANSWERS_FROM_QUESTION, question_id)

    def get_question_witch_more_than_order(self, order: int) -> list[Question]:
        questions_list = self.execute(Question.SELECT_ALL_FROM_ORDER, order, need_answer=True)
        return _list_question_from_response(questions_list)

    def update_jump(self, question_id: int, answer_id: int, destination_id: int):
        self.execute(EnableAnswers.UPDATE_JUMP, destination_id, question_id, answer_id)

    def update_circle(self, question_id: int, start_id: int, finish_id: int):
        self.execute(RepeatQuestions.DELETE_QUESTION, question_id)
        self.execute(RepeatQuestions.INSERT_REPEAT, question_id, start_id, finish_id)

    def get_patients(self) -> list[Patient]:
        return _list_patients_from_response(self.execute(Patient.SELECT_ALL, need_answer=True))

    def delete_patient(self, patient_id: int):
        self.execute(Patient.DELETE, patient_id)

    def add_answer_to_question(self, answer: str, question_id: int) -> int:
        answer_id = self._insert_entity_if_not_exist(Answer.GET_ID_BY_TEXT, answer, Answer.INSERT_INTO, answer)
        self.execute(EnableAnswers.INSERT_ANSWER, question_id, answer_id)
        return answer_id


    def delete_question_with_answer(self, question_id: int, answer_id: int):
        self.execute(EnableAnswers.DELETE_QUESTION_AND_ANSWER, question_id, answer_id)


if __name__ == "__main__":
    MedDatabase().add_patient("Ваня", 22, 0)
