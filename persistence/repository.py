import atexit
import sqlite3
from .dao import Dao
from . import dto

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

    def _create_tables(self): # TODO
        self._conn.executescript("""
                CREATE TABLE vaccines (
                    id              INTEGER     PRIMARY KEY,
                    date            DATE        NOT NULL,
                    supplier        INTEGER     REFERENCES Supplier(id),
                    quantity        INTEGER     NOT NULL
                );

                CREATE TABLE suppliers (
                    id              INTEGER     PRIMARY KEY,
                    name            STRING      NOT NULL,
                    logistic        INTEGER     REFERENCES Logistic(id)
                );

                CREATE TABLE clinics (
                    id              INTEGER     PRIMARY KEY,
                    location        STRING      NOT NULL,
                    demand          INTEGER     NOT NULL,
                    logistic        INTEGER     REFERENCES Logistic(id)
                );

                CREATE TABLE logistics (
                    id              INTEGER     PRIMARY KEY,
                    name            STRING      NOT NULL,
                    count_sent      INTEGER     NOT NULL,
                    count_received  INTEGER NOT NULL
                );
            """)


# Singleton:
repo = _Repository()
atexit.register(repo.close)
