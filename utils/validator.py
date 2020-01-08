from utils.exceptions import NotCorrectMessage

from models.exercise import Exercise


class Validator:
    @classmethod
    def validate_exercise(cls, raw_message: str) -> None:
        exercise = raw_message.strip()
        if not exercise.isalpha() or \
                exercise not in [d['name'] for d in Exercise.all()]:
            raise NotCorrectMessage('Неверное название упражнения')

    @classmethod
    def validate_level(cls, raw_message: str) -> None:
        level = raw_message.strip()
        if not level.isdigit() or int(level) not in tuple(range(1, 11)):
            raise NotCorrectMessage(
                'Номер уровня должен быть числом от 1 до 10'
            )
