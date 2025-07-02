from __future__ import annotations
from typing import TYPE_CHECKING
import sqlite3
from contextlib import contextmanager

if TYPE_CHECKING:
    from models import ResultInfoSeries, ResultInfo

class DBManager:
    def __init__(self, db_path: str="Report.db", table_name: str = "Reports"):
        self.db_path = db_path
        self.table_name = table_name

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
            cursor.close()
            connection.close()

    def create_tables(self):
        
        with self.session() as cursor:
            cursor.execute(f"DROP TABLE IF EXISTS Reports")
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS Reports (
                            id INTEGER PRIMARY KEY,
                            file_name TEXT NOT NULL,
                            name TEXT NOT NULL,
                            flag TEXT DEFAULT 'NULL',
                            value REAL DEFAULT 'NULL',
                            lower_range REAL DEFAULT 'NULL',
                            upper_range REAL DEFAULT 'NULL',
                            units TEXT DEFAULT 'NULL',
                            date TEXT DEFAULT 'NULL')""")
            
    def insert_info(self, all_records: list[ResultInfoSeries]):
        query = "INSERT INTO Reports (file_name, name, flag, value, lower_range, upper_range, units, date) VALUES (?,?,?,?,?,?,?,?)"
        params = []
        for record in all_records:
            file_name = record.report_name
            date = record.report_date
            for results in record.report_results:
                params.append((
                    file_name,
                    results.name,
                    results.flag,
                    results.value,
                    results.lower_range,
                    results.upper_range,
                    results.units,
                    date
                ))
        with self.session() as cursor:
            cursor.executemany(query, params)
                
    