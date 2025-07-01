import sqlite3
from contextlib import contextmanager

class DBManager:
    def __init__(self, db_path: str="Report.db"):
        self.db_path = db_path

    @contextmanager
    def session(self):
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.cursor()
            yield cursor
            connection.commit()
        except:
            connection.rollback()
            raise
        finally:
            connection.close()
            cursor.close()