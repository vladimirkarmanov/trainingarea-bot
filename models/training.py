import datetime
import re
from typing import NamedTuple

import pytz

from db import DbManager
import db
import exceptions
from exercises import Exercises


class Training(DbManager):
    _tablename = 'training'
    _columns = ['id', 'date']

    def add_training(raw_message: str) -> Training:
        parsed_message = _parse_message(raw_message)
        exercise = Exercises().get_exercise(parsed_message.exercise_name)
        level = Exercise().get_level_pk_by_name(parsed_message.level_name)
        exercise_repetitions = ExerciseRepetitions(pk_exercise=exercise.name,
                                                   pk_level=level.name,
                                                   repetitions=parsed_message.repetitions)
        inserted_row_id = db.insert("training", {
            "date": parsed_message.date
        })
        return Training(date=parsed_message.date,
                        pk_exercise_repetitions=exercise)

    def get_today_statistics() -> str:
        """Возвращает строкой статистику расходов за сегодня"""
        cursor = db.get_cursor()
        cursor.execute("select sum(amount)"
                       "from expense where created=current_date")
        result = cursor.fetchone()
        if not result[0]:
            return "Сегодня ещё нет расходов"
        all_today_expenses = result[0]
        cursor.execute("select sum(amount) "
                       "from expense where created=current_date "
                       "and category_codename in (select codename "
                       "from category where is_base_expense=true)")
        result = cursor.fetchone()
        base_today_expenses = result[0] if result[0] else 0
        return (f"Расходы сегодня:\n"
                f"всего — {all_today_expenses} руб.\n"
                f"базовые — {base_today_expenses} руб. из {_get_budget_limit()} руб.\n\n"
                f"За текущий месяц: /month")

    def get_month_statistics() -> str:
        """Возвращает строкой статистику расходов за текущий месяц"""
        now = _get_now_datetime()
        first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
        cursor = db.get_cursor()
        cursor.execute(f"select sum(amount) "
                       f"from expense where created >= '{first_day_of_month}'")
        result = cursor.fetchone()
        if not result[0]:
            return "В этом месяце ещё нет расходов"
        all_today_expenses = result[0]
        cursor.execute(f"select sum(amount) "
                       f"from expense where created >= '{first_day_of_month}' "
                       f"and category_codename in (select codename "
                       f"from category where is_base_expense=true)")
        result = cursor.fetchone()
        base_today_expenses = result[0] if result[0] else 0
        return (f"Расходы в текущем месяце:\n"
                f"всего — {all_today_expenses} руб.\n"
                f"базовые — {base_today_expenses} руб. из "
                f"{now.day * _get_budget_limit()} руб.")

    def last():
        """Возвращает последние несколько расходов"""
        cursor = db.get_cursor()
        cursor.execute(
            "select e.id, e.amount, c.name "
            "from expense e left join category c "
            "on c.codename=e.category_codename "
            "order by created desc limit 10")
        rows = cursor.fetchall()
        last_expenses = []
        for row in rows:
            last_expenses.append({
                'amount': row[1],
                'id': row[0],
                'category_name': row[2]
            })
        return last_expenses

    def delete_training(row_id: int) -> None:
        """Удаляет сообщение по его идентификатору"""
        db.delete("expense", row_id)

    def _get_now_formatted() -> str:
        """Возвращает сегодняшнюю дату строкой"""
        return _get_now_datetime().strftime("%Y-%m-%d")

    def _get_now_datetime() -> datetime.datetime.now:
        """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
        tz = pytz.timezone('Asia/Yekaterinburg')
        now = datetime.datetime.now(tz)
        return now

    def _get_budget_limit() -> int:
        """Возвращает дневной лимит трат для основных базовых трат"""
        return db.fetchall("budget", ["daily_limit"])[0]["daily_limit"]
