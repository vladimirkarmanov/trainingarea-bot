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
