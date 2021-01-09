import sqlite3
from dao import Dao

DATABASE_PATH = 'database.db'

class _Repository():
    def __init__(self):
        self._conn = sqlite3.connect(DATABASE_PATH)
        self._create_tables()

        self.vaccines = Dao(dto.Vaccine, self._conn)
        self.suppliers = Dao(dto.Supplier, self._conn)
        self.clinics = Dao(dto.Clinic, self._conn)
        self.logistics = Dao(dto.Logistic, self._conn)

    def close(self):
        self._conn.commit()
        self._conn.close()

    def config_table(self, table_name, data):
        '''
        data = [{
            "id":1, "name":"Tel-Aviv",
            },]
        '''
        pass


    def _create_tables(self): # TODO
        _conn.executescript("""
                CREATE TABLE vaccines (
                    id      INT         PRIMARY KEY,
                    name    TEXT        NOT NULL
                );

                CREATE TABLE suppliers (
                    num                 INT     PRIMARY KEY,
                    expected_output     TEXT    NOT NULL
                );

                CREATE TABLE clinics (
                    student_id      INT     NOT NULL,
                    assignment_num  INT     NOT NULL,
                    grade           INT     NOT NULL,

                    FOREIGN KEY(student_id)     REFERENCES students(id),
                    FOREIGN KEY(assignment_num) REFERENCES assignments(num),

                    PRIMARY KEY (student_id, assignment_num)
                );

                CREATE TABLE logistics (
                    student_id      INT     NOT NULL,
                    assignment_num  INT     NOT NULL,
                    grade           INT     NOT NULL,

                    FOREIGN KEY(student_id)     REFERENCES students(id),
                    FOREIGN KEY(assignment_num) REFERENCES assignments(num),

                    PRIMARY KEY (student_id, assignment_num)
                );
            """)


# Singleton:
repo = _Repository()
atexit.register(repo.close())
