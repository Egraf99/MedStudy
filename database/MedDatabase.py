import sqlite3
from typing import Optional

from database.entities.Entity import *


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
        self.execute(Patients.CREATE_TABLE)
        self.execute(Answers.CREATE_TABLE)
        self.execute(PatientAnswer.CREATE_TABLE)
        self.execute(Question.CREATE_TABLE)
        self.execute(EnableAnswers.CREATE_TABLE)
        self.execute(RepeatQuestions.CREATE_TABLE)

        # добавляем ответы Да и Нет с нужными id, если их еще нет в БД
        if not self.execute(Answers.GET_BOOL_ANSWERS, need_answer=True):
            self.execute(Answers.INSERT_INTO_WITH_ID, "0", "Нет")
            self.execute(Answers.INSERT_INTO_WITH_ID, "1", "Да")

    def add_patient(self, name: str, age: int, male: int):
        self.execute(Patients.INSERT_ALL, name, age, male)

    def get_last_rowid(self) -> int:
        query = """
            SELECT last_insert_rowid()
            """

        print(self.execute(query, need_answer=True)[0][0])
        return self.execute(query, need_answer=True)[0][0]

    def get_count_questions(self) -> int:
        return self.execute(Question.GET_COUNT, need_answer=True)[0][0] + 1

    def _insert_entity_if_not_exist(self, check_query: str, check_field, insert_query: str, *insert_fields) -> int:
        try:
            id_ = self.execute(check_query, check_field, need_answer=True)[0][0]
        except IndexError:
            self.execute(insert_query, *insert_fields)
            id_ = self.execute(check_query, check_field, need_answer=True)[0][0]
        return id_

    def insert_question(self, question: Question):
        single_answer: int = 1 if question.type_ != Question.TypeAnswer.MANY else 0
        question_id = self._insert_entity_if_not_exist(Question.GET_ID_BY_NAME, question.name,
                                                       Question.INSERT,
                                                       question.name, question.short, single_answer,
                                                       question.require_int, question.private_int, question.order)
        if question.type_ == Question.TypeAnswer.BOOL:
            self.execute(EnableAnswers.INSERT_NO_ANSWER, question_id)
            self.execute(EnableAnswers.INSERT_YES_ANSWER, question_id)
        else:
            self.execute(Question.UPDATE_MEASURE, question.measure, question_id)
            if question.type_ == Question.TypeAnswer.MANY and question.list_answers:
                for answer in question.list_answers:
                    answer_id = self._insert_entity_if_not_exist(Answers.GET_ID_BY_TEXT, answer, Answers.INSERT_INTO,
                                                                 answer)
                    self.execute(EnableAnswers.INSERT_ANSWER, question_id, answer_id)

    def get_questions_order(self):
        questions_list = self.execute(Question.SELECT_ORDER, need_answer=True)
        return list(
            map(lambda question: Question(id_=question[0],
                                          name=question[1],
                                          short=question[2],
                                          single_answer=question[3],
                                          require=question[4],
                                          measure=question[5],
                                          private=question[6],
                                          order=question[7]
                                          ),
                questions_list))


if __name__ == "__main__":
    MedDatabase().add_patient("Ваня", 22, 0)
