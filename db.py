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
            
    def insert_info(self, all_chosen_records: list[ResultInfoSeries]):
        query = "INSERT INTO Reports (file_name, name, flag, value, lower_range, upper_range, units, date) VALUES (?,?,?,?,?,?,?,?)"
        params = []
        for record in all_chosen_records:
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

    def select_shared_names(self) -> list[str]:
        """
        Select all names from Reports that are shared by each unique file_name.

        Returns:
            shared_names: A list of the shared names.
        """

        query = """
        SELECT name FROM Reports
        GROUP BY name
        HAVING COUNT(DISTINCT file_name) = (
            SELECT COUNT(DISTINCT file_name)
            FROM Reports
        )
        """            

        with self.session() as cursor:
            cursor.execute(query)
            shared_names = [row[0] for row in cursor.fetchall()]

        return shared_names
    
    def select_values_for_name(self, name: str) -> tuple[str, float, float, float, str, str, str]:
        """
        Selects column information from the table at the given name.

        Args:
            name: name of a name in the database.

        Returns:
            values: Selected values from data base at 'name'.
        """
        query = """
        SELECT name, flag, value, lower_range, upper_range, units, file_name, date 
        FROM Reports
        WHERE name=?
        ORDER BY date
        """

        with self.session() as cursor:
            cursor.execute(query, (name,))
            values = cursor.fetchall()
        return values