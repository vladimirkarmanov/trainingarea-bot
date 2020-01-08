from typing import List, Dict
import re


class Parser:
    @staticmethod
    def obj_to_string(obj: Dict) -> str:
        result = ''
        for val in obj.values():
            result += '\n' + val
        return result

    @staticmethod
    def list_objs_to_string(objs: List[dict]) -> str:
        result = ''
        for obj in objs:
            result += Parser.obj_to_string(obj)
        return result
