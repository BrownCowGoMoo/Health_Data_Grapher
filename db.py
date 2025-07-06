import sqlite3
from contextlib import contextmanager

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
            cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id INTEGER PRIMARY KEY,
                    file_name TEXT NOT NULL,
                    name TEXT NOT NULL,
                    flag TEXT DEFAULT 'NULL',
                    value REAL DEFAULT 'NULL',
                    lower_range REAL DEFAULT 'NULL',
                    upper_range REAL DEFAULT 'NULL',
                    units TEXT DEFAULT 'NULL',
                    date TEXT DEFAULT 'NULL'
                )
            """)

    def insert_info(self, all_series: list[dict]):
        """
        all_series: list of dicts with keys
            'report_name': str,
            'report_date': datetime or None,
            'report_results': list of dicts each having
                'name', 'flag', 'value', 'lower_range',
                'upper_range', 'units'
        """
        query = (
            f"INSERT INTO {self.table_name} "
            "(file_name, name, flag, value, lower_range, upper_range, units, date) "
            "VALUES (?,?,?,?,?,?,?,?)"
        )
        params = []
        for series in all_series:
            fname = series["report_name"]
            date_obj = series["report_date"]
            date_str = date_obj.strftime("%Y-%m-%d %H:%M") if date_obj else ""
            for result in series["report_results"]:
                params.append((
                    fname,
                    result["name"],
                    result["flag"],
                    result["value"],
                    result["lower_range"],
                    result["upper_range"],
                    result["units"],
                    date_str
                ))

        with self.session() as cursor:
            cursor.executemany(query, params)

    def select_shared_names(self) -> list[str]:
        """
        Select all names from Reports that are shared by each unique file_name.
        """
        query = f"""
            SELECT name
            FROM {self.table_name}
            GROUP BY name
            HAVING COUNT(DISTINCT file_name) = (
                SELECT COUNT(DISTINCT file_name)
                FROM {self.table_name}
            )
        """
        with self.session() as cursor:
            cursor.execute(query)
            return [row[0] for row in cursor.fetchall()]

    def select_values_for_name(self, name: str) -> list[tuple]:
        """
        Returns list of tuples:
            (name, flag, value, lower_range, upper_range, units, file_name, date)
        """
        query = f"""
            SELECT name, flag, value, lower_range, upper_range, units, file_name, date
            FROM {self.table_name}
            WHERE name = ?
            ORDER BY date
        """
        with self.session() as cursor:
            cursor.execute(query, (name,))
            return cursor.fetchall()