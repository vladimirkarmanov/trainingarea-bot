from typing import Dict, List

from db import DbManager, get_cursor


class Exercise(DbManager):
    _tablename = 'exercise'
    _columns = ['name']
    