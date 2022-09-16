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
            print(script, args)
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
        self.execute(Questions.CREATE_TABLE)
        self.execute(EnableAnswers.CREATE_TABLE)

    def add_patient(self, name: str, age: int, male: int):
        self.execute(Patients.INSERT_ALL, name, age, male)


if __name__ == "__main__":
    MedDatabase().add_patient("Ваня", 22, 0)
