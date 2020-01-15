from aiogram.dispatcher.filters.state import State, StatesGroup


class LevelStates(StatesGroup):
    exercise = State()
    level_num = State()
