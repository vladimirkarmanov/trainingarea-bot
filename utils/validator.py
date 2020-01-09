from datetime import datetime

from models.exercise import Exercise
from utils.exceptions import NotCorrectMessage


class Validator:
    @classmethod
    def clean_exercise(cls, raw_message: str) -> str:
        exercise = raw_message.strip()
        if not exercise.isalpha() or \
            exercise not in [d['name'] for d in Exercise.all()]:
            raise NotCorrectMessage('Неверное название упражнения')
        return exercise

    @classmethod
    def clean_level(cls, raw_message: str) -> str:
        level = raw_message.strip()
        if not level.isdigit() or int(level) not in tuple(range(1, 11)):
            raise NotCorrectMessage(
                'Номер уровня должен быть числом от 1 до 10'
            )
        return level

    @classmethod
    def clean_date(cls, raw_message: str) -> str:
        try:
            date = raw_message.strip()
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise NotCorrectMessage('Дата должна быть в формате YYYY-MM-DD')
        else:
            return date

    @classmethod
    def clean_repetitions(cls, repetitions: str) -> str:
        try:
            for rep in repetitions.split(' '):
                if not rep.isdigit():
                    raise NotCorrectMessage('Повторы должны быть числами')
        except ValueError:
            raise NotCorrectMessage('Необходим данный формат\n'
                                    'упражнение1 - 15 20 10 12\n'
                                    'упражнение2 - 50 55 48')
        else:
            return repetitions
