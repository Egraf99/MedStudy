import sqlite3
from typing import Optional

from database.entities.Entity import *


class MedDatabase:
    NAME_DB: str = "./database/med.db"

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

    def insert_question(self, question: Question):
        single_answer: int = 1 if question.type_ != Question.TypeAnswer.MANY else 0
        require = 1 if question.require else 0
        private = 1 if question.private else 0
        try:
            question_id = self.execute(Question.GET_ID_BY_NAME, question.name, need_answer=True)[0][0]
        except IndexError:
            self.execute(Question.INSERT,
                         question.name, question.short, single_answer, require, private, question.order)
            question_id = self.execute(Question.GET_ID_BY_NAME, question.name, need_answer=True)[0][0]
        if question.type_ == Question.TypeAnswer.BOOL:
            self.execute(EnableAnswers.INSERT_NO_ANSWER, question_id)
            self.execute(EnableAnswers.INSERT_YES_ANSWER, question_id)
        else:
            self.execute(Question.UPDATE_MEASURE, question.measure, question_id)
            if question.type_ == Question.TypeAnswer.MANY and question.list_answers:
                for answer in question.list_answers:
                    try:
                        answer_id = self.execute(Answers.GET_ID_BY_TEXT, answer, need_answer=True)[0][0]
                    except IndexError:
                        self.execute(Answers.INSERT_INTO, answer)
                        answer_id = self.execute(Answers.GET_ID_BY_TEXT, answer, need_answer=True)[0][0]
                    self.execute(EnableAnswers.INSERT_ANSWER, question_id, answer_id)


if __name__ == "__main__":
    MedDatabase().add_patient("Ваня", 22, 0)
