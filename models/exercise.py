from db import DbManager


class Exercise(DbManager):
    _tablename = 'exercise'
    _columns = ['name']
