from db import DbManager


class ExerciseRepetitions(DbManager):
    _tablename = 'exercise_repetitions'
    _columns = ['id', 'pk_training', 'pk_exercise', 'pk_level', 'repetitions']

    @classmethod
    def add_exercise_repetitions(cls,
                                 pk_training: int,
                                 pk_exercise: str,
                                 pk_level: str,
                                 repetitions: str) -> None:
        cls.insert(
            {'pk_training': pk_training,
             'pk_exercise': pk_exercise,
             'pk_level': pk_level,
             'repetitions': repetitions}
        )
