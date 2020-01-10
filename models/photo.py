import os
from typing import List

from config import MEDIA_ROOT
from db import DbManager


class Photo(DbManager):
    _tablename = 'photo'
    _columns = ['filepath', 'pk_level']

    @classmethod
    def get_photos_for_level(cls, level_name: str) -> List[str]:
        photos = cls.filter(field='pk_level', value=level_name)
        return [os.path.join(MEDIA_ROOT, p.get('filepath')) for p in photos]
