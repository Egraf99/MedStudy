from enum import Enum


class Patient:
    def __init__(self, id_: int, name: str, male: int, age: int):
        self.id = id_
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
        INSERT INTO Patients (name, age, male) VALUES (?,?,?)
        """

    GET_COUNT: str = """
        SELECT COUNT(*) FROM Patients
        """

    SELECT_ALL: str = """
        SELECT * FROM Patients ORDER BY name ASC
        """

    DELETE: str = """
        DELETE FROM Patients WHERE id = ?
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

    def __repr__(self):
        return str(self.name)


class NoAnswer(Answer):
    def __init__(self):
        super().__init__(-1, "None")


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
            start INTEGER NOT NULL DEFAULT 0 CHECK (start IN (0,1)),
            next_question_id INTEGER NOT NULL DEFAULT -1,
            block INTEGER NOT NULL DEFAULT 0,
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

    UPDATE_NEXT_QUESTION: str = """
        UPDATE Question SET next_question_id = ? WHERE id = ?
        """

    UPDATE_BLOCK_AND_SET_START_ZERO: str = """
        UPDATE Question SET block = ?, start = 0 WHERE id = ?
        """

    UPDATE_BLOCK_AND_SET_NEXT_QUESTION: str = """
        UPDATE Question SET block = ?, next_question_id = ? WHERE id = ?
        """

    UPDATE_SET_NEW_START: str = """
        UPDATE Question SET start = 1 WHERE id = ?
        """

    SET_START: str = """
        UPDATE Question SET start = 1 WHERE id = ?
        """

    SET_STOP: str = """
        UPDATE Question SET next_question_id = -1 WHERE id = ?
        """

    SET_STOP_INSTEAD_QUESTION: str = """
        UPDATE Question SET next_question_id = -1 WHERE next_question_id = ?
        """

    SET_STOP_WHERE_NEXT_QUESTION: str = """
        UPDATE Question SET next_question_id = -1 WHERE next_question_id = ?
        """

    SET_NEW_NEXT_QUESTION: str = """
        UPDATE Question SET next_question_id = (SELECT next_question_id FROM Question WHERE id = ?) WHERE id = ?
        """

    DELETE_BY_ID: str = """
        DELETE FROM Question WHERE id = ?
        """

    UPDATE_CHAIN_DELETE: str = """
        UPDATE Question
        SET next_question_id = 
            (SELECT next_question_id 
             FROM Question 
             WHERE question_id = ?) 
        WHERE question_id = ?
        """

    UPDATE_ORDER: str = """
        UPDATE Question SET order_int = order_int - 1 WHERE order_int > ?
        """

    SELECT_ORDER_BY_ID: str = """
        SELECT order_int FROM Question WHERE id = ?
        """

    SELECT_ALL_ORDER_ASC: str = """
        SELECT * FROM Question ORDER BY id ASC
        """

    SELECT_ALL_FROM_ORDER: str = """
        SELECT * FROM Question WHERE order_int > ? ORDER BY order_int ASC
        """

    GET: str = """
        SELECT * FROM Question WHERE id = ?
        """

    GET_PREV: str = """
        SELECT * FROM Question WHERE next_question_id = ?
        """

    GET_LAST: str = """
        SELECT * FROM Question WHERE next_question_id = -1 AND block = ?
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
            private 
            )
        VALUES (?,?,?,?,?,?)"""

    GET_ID_BY_NAME: str = """
        SELECT id FROM Question WHERE name = ?
        """

    class TypeAnswer(Enum):
        BOOL = 0
        SINGLE = 1
        MANY = 2
        INTEGER = 3
        FLOAT = 4
        TEXT = 5

    def __init__(self,
                 id_: int = None,
                 name: str = None,
                 short: str = None,
                 type_: int = None,
                 require: int = 0,
                 measure: str = None,
                 private: int = 0,
                 start: int = 0,
                 next_question_id: int = -1,
                 block: int = 0
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
        self.start: bool = bool(start)
        self.next_question_id = next_question_id
        self.block = block
        self.list_answers = None

    def set_enable_answers(self, list_answers: list[str] = None):
        if list_answers:
            self.list_answers = list_answers

    def __repr__(self):
        return str(self.name)

    def __eq__(self, other):
        if type(other) == Question:
            return self.id_ == other.id_
        else:
            return False


class PatientAnswer:
    CREATE_TABLE: str = """
        CREATE TABLE IF NOT EXISTS PatientAnswer (
            patient_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            answer_id INTEGER NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES Patient(id),
            FOREIGN KEY (question_id) REFERENCES Question(id),
            FOREIGN KEY (answer_id) REFERENCES Answer(id),
            UNIQUE (patient_id, question_id, answer_id)
        )
        """


class EnableAnswers:
    CREATE_TABLE: str = """
        CREATE TABLE IF NOT EXISTS EnableAnswers (
            question_id INTEGER NOT NULL,
            answer_id INTEGER,
            jump_to_question INTEGER,
            cycle INTEGER NOT NULL DEFAULT 0 CHECK (cycle IN (0,1)),
            FOREIGN KEY (question_id) REFERENCES Question(id),
            FOREIGN KEY (answer_id) REFERENCES Answer(id)
        )
        """

    DELETE_QUESTION: str = """
        DELETE FROM EnableAnswers WHERE question_id = ? 
        """

    DELETE_JUMP: str = """
        DELETE FROM EnableAnswers WHERE jump_to_question = ? 
        """
    DELETE_QUESTION_AND_ANSWER: str = """
        DELETE FROM EnableAnswers WHERE question_id = ? AND answer_id = ?
        """

    DELETE_QUESTION_WITH_NONE_ANSWER: str = """
        DELETE FROM EnableAnswers WHERE question_id = ? AND answer_id IS NULL
        """

    ADD_BRANCH_TO_QUESTION: str = """
        INSERT INTO EnableAnswers (question_id, jump_to_question, cycle) VALUES (?,?,?)
        """

    ADD_BRANCH_TO_QUESTION_ANSWER: str = """
        INSERT INTO EnableAnswers (question_id, answer_id, jump_to_question, cycle) VALUES (?,?,?,?)
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

    GET_JUMP_BY_QUESTION_AND_ANSWER: str = """
        SELECT * FROM Question WHERE id = (
            SELECT jump_to_question FROM EnableAnswers WHERE question_id = ? AND answer_id = ?
            )
        """

    GET_JUMP_BY_QUESTION_WITH_NONE_ANSWER: str = """
        SELECT * FROM Question WHERE id = (
            SELECT jump_to_question FROM EnableAnswers WHERE question_id = ? AND answer_id IS NULL
            )
        """

    SELECT_BY_QUESTION_ID: str = """
        SELECT ea.answer_id, a.name 
        FROM EnableAnswers ea
        INNER JOIN Answer a ON ea.answer_id = a.id
        WHERE ea.question_id = ?
        """

    SELECT_CYCLE_BY_QUESTION_ID: str = """
        SELECT ea.answer_id, a.name, ea.jump_to_question, ea.cycle 
        FROM EnableAnswers ea
        LEFT JOIN Answer a ON ea.answer_id = a.id
        LEFT JOIN Question q ON ea.jump_to_question = q.id
        WHERE question_id = ?
        """

    DELETE_ANSWERS_FROM_QUESTION: str = """
        DELETE FROM EnableAnswers WHERE question_id = ?
        """

    UPDATE_JUMP: str = """
        UPDATE EnableAnswers SET jump_to_question = ? WHERE question_id = ? AND answer_id =?
        """

    UPDATE_JUMP_QUESTION: str = """
        UPDATE EnableAnswers SET jump_to_question = ? WHERE jump_to_question = ?
        """


class BranchQuestions:
    CREATE_TABLE: str = """
        CREATE TABLE IF NOT EXISTS BranchQuestions (
            question_id INTEGER NOT NULL,
            answer_id INTEGER,
            from_question INTEGER NOT NULL,
            to_question INTEGER NOT NULL,
            cycle INTEGER DEFAULT 0 CHECK (cycle IN (0,1)),
            FOREIGN KEY (question_id) REFERENCES Question(id),
            FOREIGN KEY (from_question) REFERENCES Question(id),
            FOREIGN KEY (to_question) REFERENCES Question(id),
            FOREIGN KEY (answer_id) REFERENCES Answer(id)
        ) 
        """

    UPDATE_TABLE: str = """
        """

    DELETE_QUESTION_WITH_ANSWER: str = """
        DELETE FROM BranchQuestions WHERE question_id = ? AND answer_id = ?
        """

    INSERT_BRANCH: str = """
        INSERT INTO BranchQuestions (question_id, answer_id, from_question, to_question, cycle)
        VALUES (?,?,?,?,?)
        """

    DELETE_ANSWERS_FROM_QUESTION: str = """
        DELETE FROM BranchQuestions WHERE question_id = ?
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
            (2, "many"),
            (3, "count")
        """

    GET_TYPES: str = """
        SELECT * FROM QuestionType WHERE id IN (0,1,2)
        """


if __name__ == '__main__':
    pat = Patient("Egor", 23, 0)
    print(pat.male)
