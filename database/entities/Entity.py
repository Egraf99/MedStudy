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


class Answer:
    CREATE_TABLE: str = """
        CREATE TABLE IF NOT EXISTS Answer (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        """

    INSERT_BOOL_ANSWER: str = """
        INSERT INTO Answer (id, name) VALUES 
            (0, "Нет"),
            (1, "Да")
        """

    INSERT_INTO: str = """
        INSERT INTO Answer (name) VALUES (?)
        """

    GET_BOOL_ANSWERS: str = """
        SELECT * FROM Answer WHERE id IN (0,1)
        """

    GET_ID_BY_TEXT: str = """
        SELECT id FROM Answer WHERE name = ?
        """

    def __init__(self,
                 id_: int,
                 name: str):
        self.id_ = id_
        self.name = name


class Question:
    CREATE_TABLE: str = """
        CREATE TABLE IF NOT EXISTS Question ( 
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            short TEXT,
            type_answer INTEGER NOT NULL DEFAULT 0,
            require INTEGER NOT NULL DEFAULT 0 CHECK (require IN (0,1)),
            measure TEXT,
            private INTEGER NOT NULL DEFAULT 0 CHECK (private IN (0,1)),
            order_int INTEGER NOT NULL UNIQUE,
            FOREIGN KEY (type_answer) REFERENCES QuestionType(id)
        )"""

    UPDATE_QUESTION: str = """
        UPDATE Question SET 
            name = ?,
            short = ?,
            type_answer = ?,
            measure = ?,
            require = ?,
            private = ? 
        WHERE id = ?"""

    SELECT_ORDER: str = """
        SELECT * FROM Question ORDER BY order_int ASC
        """

    GET_COUNT: str = """
        SELECT COUNT(*) FROM Question
        """

    INSERT: str = """
        INSERT INTO Question (
            name,
            short, 
            type_answer, 
            measure,
            require,
            private, 
            order_int
            )
        VALUES (?,?,?,?,?,?,?)"""

    GET_ID_BY_NAME: str = """
        SELECT id FROM Question WHERE name = ?
        """

    def __init__(self,
                 id_: int = None,
                 name: str = None,
                 short: str = None,
                 type_: int = None,
                 require: int = 0,
                 measure: str = None,
                 private: int = 0,
                 order: int = None,
                 ):
        self.id_ = id_
        self.name: str = name
        self.short: str = short
        self.type_ = type_
        self.measure = measure
        self.require_int: int = require
        self.require_bool: bool = bool(require)
        self.private_int: int = private
        self.private_bool: bool = bool(private)
        self.order: int = order
        self.list_answers = None

    def set_enable_answers(self, list_answers: list[str] = None):
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


class EnableAnswers:
    CREATE_TABLE: str = """
        CREATE TABLE IF NOT EXISTS EnableAnswers (
            question_id INTEGER NOT NULL,
            answer_id INTEGER NOT NULL,
            jump_to_question INTEGER,
            FOREIGN KEY (question_id) REFERENCES Question(id),
            FOREIGN KEY (answer_id) REFERENCES Answer(id)
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

    SELECT_BY_QUESTION_ID: str = """
        SELECT ea.answer_id, a.name 
        FROM EnableAnswers ea
        INNER JOIN Answer a ON ea.answer_id = a.id
        WHERE ea.question_id = ?
        """

    DELETE_ANSWERS_FROM_QUESTION: str = """
        DELETE FROM EnableAnswers WHERE question_id = ?
        """


class RepeatQuestions:
    CREATE_TABLE: str = """
        CREATE TABLE IF NOT EXISTS RepeatQuestions (
            question_id INTEGER NOT NULL UNIQUE,
            from_question INTEGER NOT NULL,
            to_question INTEGER NOT NULL
        ) 
        """


class QuestionType:
    CREATE_TABLE: str = """
        CREATE TABLE IF NOT EXISTS QuestionType (
            id INTEGER NOT NULL,
            type TEXT NOT NULL UNIQUE
        )"""

    INSERT_TYPES: str = """
        INSERT INTO QuestionType (id, type) VALUES  
            (0, "bool"),
            (1, "single"),
            (2, "many")
        """

    GET_TYPES: str = """
        SELECT * FROM QuestionType WHERE id IN (0,1,2)
        """


if __name__ == '__main__':
    pat = Patients("Egor", 23, 0)
    print(pat.male)
