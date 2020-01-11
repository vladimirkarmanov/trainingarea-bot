from aiogram.dispatcher.filters.state import State, StatesGroup


class LevelStates(StatesGroup):
    exercise = State()
    level_num = State()


class TrainingStates(StatesGroup):
    date = State()
    exercises_repetitions = State()
