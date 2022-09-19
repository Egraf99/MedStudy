from enum import Enum


class Patients:
    def __init__(self, name: str, age: int, male: int):
        self.name = name
        self.age = age
        self.male = male

    CREATE_TABLE: str = """
        CREATE TABLE IF NOT EXISTS Patients ( 
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            male INTEGER DEFAULT 1 CHECK (male IN (0,1)),
            age INTEGER NOT NULL CHECK (age > 0)
        )"""

    INSERT_ALL: str = """
        INSERT INTO Patient (name, age, male) VALUES (?,?,?)
        """

    GET_COUNT: str = """
        SELECT COUNT(*) FROM Patients
        """


class Question:
    class TypeAnswer(Enum):
        BOOL = 0
        SINGLE = 1
        MANY = 2

    CREATE_TABLE: str = """
        CREATE TABLE IF NOT EXISTS Question ( 
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL UNIQUE,
            short TEXT,
            single_answer INTEGER NOT NULL DEFAULT 1 CHECK (single_answer IN (0,1)),
            require INTEGER NOT NULL DEFAULT 0 CHECK (require IN (0,1)),
            measure TEXT,
            private INTEGER NOT NULL DEFAULT 0 CHECK (private IN (0,1)),
            order_int INTEGER NOT NULL UNIQUE
        )"""

    GET_COUNT: str = """
        SELECT COUNT(*) FROM Question
        """

    INSERT: str = """
        INSERT INTO Question (
            question,
            short, 
            single_answer, 
            require, 
            private, 
            order_int
            )
        VALUES (?,?,?,?,?,?)"""

    UPDATE_MEASURE: str = """
        UPDATE Question SET measure = ? WHERE id = ?
        """

    GET_ID_BY_NAME: str = """
        SELECT id FROM Question WHERE question = ?
        """

    def __init__(self,
                 name: str = None,
                 short: str = None,
                 require: bool = False,
                 private: bool = False,
                 order: int = None):
        self.name: str = name
        self.short: str = short
        self.type_ = Question.TypeAnswer.BOOL
        self.require: bool = require
        self.private: bool = private
        self.order: int = order
        self.measure = None
        self.list_answers = None

    def set_type(self, type_: TypeAnswer, measure: str = None, list_answers: list[str] = None):
        self.type_: Question.TypeAnswer = type_
        self.measure: str = measure
        if list_answers:
            self.list_answers = list_answers


class PatientAnswer:
    CREATE_TABLE: str = """
        CREATE TABLE IF NOT EXISTS PatientAnswer (
            patient_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            answer_id INTEGER NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES Patients(id),
            FOREIGN KEY (question_id) REFERENCES Question(id),
            FOREIGN KEY (answer_id) REFERENCES Answer(id),
            UNIQUE (patient_id, question_id, answer_id)
        )
        """


class Answers:
    CREATE_TABLE: str = """
        CREATE TABLE IF NOT EXISTS Answers (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            answer TEXT NOT NULL UNIQUE
        )
        """

    INSERT_INTO_WITH_ID: str = """
        INSERT INTO Answers (id, answer) VALUES (?,?)
        """

    INSERT_INTO: str = """
        INSERT INTO Answers (answer) VALUES (?)
        """

    GET_BOOL_ANSWERS: str = """
        SELECT * FROM Answers WHERE id IN (0,1)
        """

    GET_ID_BY_TEXT: str = """
        SELECT id FROM Answers WHERE answer = ?
        """


class EnableAnswers:
    CREATE_TABLE: str = """
        CREATE TABLE IF NOT EXISTS EnableAnswers (
            question_id INTEGER NOT NULL,
            answer_id INTEGER NOT NULL,
            jump_to_question INTEGER,
            FOREIGN KEY (question_id) REFERENCES Question(id),
            FOREIGN KEY (answer_id) REFERENCES Answers(id)
        )
        """

    INSERT_NO_ANSWER: str = """
        INSERT INTO EnableAnswers (question_id, answer_id) VALUES (?,0);
        """

    INSERT_YES_ANSWER: str = """
        INSERT INTO EnableAnswers (question_id, answer_id) VALUES (?,1);
        """

    INSERT_ANSWER: str = """
        INSERT INTO EnableAnswers (question_id, answer_id) VALUES (?,?)
        """


class RepeatQuestions:
    CREATE_TABLE: str = """
        CREATE TABLE IF NOT EXISTS RepeatQuestions (
            question_id INTEGER NOT NULL,
            from_question INTEGER NOT NULL,
            to_question INTEGER NOT NULL
        ) 
        """


if __name__ == '__main__':
    pat = Patients("Egor", 23, 0)
    print(pat.male)
