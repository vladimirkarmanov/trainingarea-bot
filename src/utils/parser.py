from typing import List, Dict


class Parser:
    @classmethod
    def obj_to_string(cls, obj: Dict) -> str:
        result = ''
        for val in obj.values():
            result += '\n' + str(val)
        return result

    @classmethod
    def list_objs_to_string(cls, objs: List[dict]) -> str:
        result = ''
        for obj in objs:
            result += Parser.obj_to_string(obj)
        return result
