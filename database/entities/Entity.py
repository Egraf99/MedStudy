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


class Questions:
    CREATE_TABLE: str = """
        CREATE TABLE IF NOT EXISTS Questions ( 
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            short TEXT,
            one_answer INTEGER NOT NULL DEFAULT 1 CHECK (one_answer IN (0,1)),
            require INTEGER NOT NULL DEFAULT 0 CHECK (require IN (0,1)),
            measure TEXT,
            private INTEGER NOT NULL DEFAULT 0 CHECK (private IN (0,1)),
            order_int INTEGER NOT NULL UNIQUE
        )"""


class PatientAnswer:
    CREATE_TABLE: str = """
        CREATE TABLE IF NOT EXISTS PatientAnswer (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            answer_id INTEGER NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES Patients(id),
            FOREIGN KEY (question_id) REFERENCES Questions(id),
            FOREIGN KEY (answer_id) REFERENCES Answer(id),
            UNIQUE (patient_id, question_id, answer_id)
        )
        """


class Answers:
    CREATE_TABLE: str = """
        CREATE TABLE IF NOT EXISTS Answers (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            answer TEXT NOT NULL
        )
        """

    INSERT_INTO_WITH_ID: str = """
        INSERT INTO Answers (id, answer) VALUES (?,?)
        """


class EnableAnswers:
    CREATE_TABLE: str = """
        CREATE TABLE IF NOT EXISTS EnableAnswers (
            question_id INTEGER NOT NULL,
            answer_id INTEGER NOT NULL,
            jump_to_question INTEGER,
            FOREIGN KEY (question_id) REFERENCES Questions(id),
            FOREIGN KEY (answer_id) REFERENCES Answers(id),
            UNIQUE (question_id, answer_id)
        )
        """


if __name__ == '__main__':
    pat = Patients("Egor", 23, 0)
    print(pat.male)
