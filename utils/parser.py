from typing import List, Dict

from utils.exceptions import NotCorrectMessage


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

    @classmethod
    def parse_exercises_repetitions(cls, raw_message: str) -> List[tuple]:
        try:
            temp_lst = raw_message.strip().split('\n')
            result = []
            for item in temp_lst:
                exercise_level, repetitions = item.split('-')
                exercise = exercise_level.split('(')[0]
                level = exercise_level.split('(')[1][0]
                result.append(
                    (exercise.strip(), level.strip(), repetitions.strip())
                )
        except (ValueError, IndexError) as e:
            raise NotCorrectMessage('Необходим данный формат:\n'
                                    'упражнение1(7 уровень) - 15 20 10 12\n'
                                    'упражнение2(4 уровень) - 50 55 48')
        else:
            return result
