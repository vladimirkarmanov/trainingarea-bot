from typing import Dict

from db import DbManager, get_cursor


class Level(DbManager):
    _tablename = 'level'
    _columns = ['name', 'description', 'easy', 'middle', 'pro', 'pk_exercise']

    @classmethod
    def level_for_exercise(cls, exercise_name: str, level_num: str) -> Dict:
        cursor = get_cursor()
        cursor.execute(
            f'SELECT * FROM {cls._tablename} '
            f'WHERE pk_exercise="{exercise_name}" AND name LIKE "%{level_num}:%"'
        )
        row = cursor.fetchone()
        columns = ['name', 'description', 'easy', 'middle', 'pro']
        return cls.row_to_dict(row, columns)

    @classmethod
    def get_formatted_level(cls, obj: Dict) -> str:
        result = (f"<b>{obj['name'].upper()}</b>\n"
                  f"{obj['description']}\n"
                  f"<ins>Легкий: {obj['easy']}</ins>\n"
                  f"<ins>Средний: {obj['middle']}</ins>\n"
                  f"<ins>Условие перехода: {obj['pro']}</ins>")
        return result
