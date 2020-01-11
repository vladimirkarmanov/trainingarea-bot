from typing import Dict

from db import DbManager
from models.exercise_repetitions import ExerciseRepetitions
from models.exercise import Exercise
from models.level import Level


class Training(DbManager):
    _tablename = 'training'
    _columns = ['id', 'date']

    @classmethod
    def add_training(cls, date: str) -> None:
        cls.insert({'date': date})

    @classmethod
    def get_formatted_training(cls, obj: Dict) -> str:
        exercise_repetitions = ExerciseRepetitions.filter(field='pk_training',
                                                          value=obj['id'])
        temp = []
        for ex in exercise_repetitions:
            exercise = Exercise.get(field='name', value=ex['pk_exercise'])
            level = Level.get(field='name', value=ex['pk_level'])
            s = f"{exercise.get('name')}({level.get('name')}):\n" \
                f"{ex.get('repetitions')}\n"
            temp.append(s)

        result = f"<b>[{obj['date']}]</b>\n"
        for t in temp:
            result += t
        return result + '\n'
