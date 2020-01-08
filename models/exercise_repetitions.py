from db import DbManager


class ExerciseRepetitions(DbManager):
    _tablename = 'exercise_repetitions'
    _columns = ['id', 'pk_training', 'repetitions', 'pk_exercise', 'pk_level']
