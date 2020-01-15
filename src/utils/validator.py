from models.exercise import Exercise
from utils.exceptions import NotCorrectMessage


class Validator:
    @classmethod
    def clean_exercise(cls, raw_message: str) -> str:
        exercise = raw_message.strip().lower()
        if not exercise.isalpha() or \
            exercise not in [d.get('name') for d in Exercise.all()]:
            raise NotCorrectMessage('Неверное название упражнения')
        return exercise

    @classmethod
    def clean_level(cls, raw_message: str) -> str:
        level = raw_message.strip().lower()
        if not level.isdigit() or int(level) not in tuple(range(1, 11)):
            raise NotCorrectMessage(
                'Номер уровня должен быть числом от 1 до 10'
            )
        return level
