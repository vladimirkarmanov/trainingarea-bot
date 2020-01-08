import os
import sqlite3
from typing import Dict, List, Tuple, Any

from config import BASE_DIR

conn = sqlite3.connect('training.db')
cursor = conn.cursor()


class DbManager:
    _tablename = None
    _columns = None

    @classmethod
    def _row_to_dict(cls, row: Tuple, columns: List[str]) -> Dict:
        if row is not None:
            return {column: row[i] for i, column in enumerate(columns)}
        return {}

    @classmethod
    def _rows_to_list(cls, rows: List[tuple], columns: List[str]) -> List[dict]:
        return [cls._row_to_dict(row, columns) for row in rows]

    @classmethod
    def get(cls, field: str, value: any) -> Dict:
        cursor.execute(
            f'SELECT * FROM {cls._tablename} WHERE {field}="{value}"'
        )
        row = cursor.fetchone()
        return cls._row_to_dict(row, cls._columns)

    @classmethod
    def all(cls) -> List[dict]:
        cursor.execute(
            f'SELECT * FROM {cls._tablename}'
        )
        rows = cursor.fetchall()
        return cls._rows_to_list(rows, cls._columns)

    @classmethod
    def filter(cls, field: str, value: any) -> List[dict]:
        cursor.execute(
            f'SELECT * from {cls._tablename} WHERE {field}="{value}"'
        )
        rows = cursor.fetchall()
        return cls._rows_to_list(rows, cls._columns)

    @classmethod
    def insert(cls, column_values: Dict) -> None:
        columns = ', '.join(column_values.keys())
        values = [tuple(column_values.values())]
        placeholders = ', '.join('?' * len(column_values.keys()))
        cursor.executemany(
            f'INSERT INTO {cls._tablename} '
            f'({columns}) '
            f'VALUES ({placeholders})',
            values)
        conn.commit()

    @classmethod
    def delete(cls, row_pk: any) -> None:
        cursor.execute(f'DELETE FROM {cls._tablename} '
                       f'WHERE {cls._columns[0]}="{row_pk}"')
        conn.commit()


def get_cursor():
    return cursor


def _init_db():
    with open(os.path.join(BASE_DIR, 'createdb.sql'), 'r') as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    cursor.execute('SELECT name FROM sqlite_master '
                   'WHERE type="table" AND name="training"')
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


if __name__ == '__main__':
    check_db_exists()
