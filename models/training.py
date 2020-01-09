from db import DbManager


class Training(DbManager):
    _tablename = 'training'
    _columns = ['id', 'date']

    @classmethod
    def add_training(cls, date: str):
        cls.insert({'date': date})
