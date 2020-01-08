from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from models.exercise import Exercise
from models.level import Level
from app import dp
from states import LevelStates
from utils.exceptions import NotCorrectMessage
from utils.parser import Parser


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(
        'Бот для программы тренировок "Тренировочная зона"\n\n'
        'Показать упражнения: /exercises\n'
        'Показать уровень для упражнения: /level'
    )


@dp.message_handler(commands=['exercises'])
async def exercises_list(message: types.Message):
    exercises = Exercise.all()
    answer_message = Parser.list_objs_to_string(exercises)
    await message.answer(answer_message)


@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info(f'Cancelling state {current_state}')
    await state.finish()
    await message.answer('Отмена')


@dp.message_handler(commands=['level'])
async def process_get_level(message: types.Message, state: FSMContext):
    await LevelStates.exercise.set()
    await message.answer('Введите название упражнения для '
                         'которого вы хотите посмотреть уровень')


@dp.message_handler(lambda message: not message.text.strip().isalpha(),
                    state=LevelStates.exercise)
async def process_exercise_invalid(message: types.Message):
    return await message.answer('Неверное название упражнения!')


@dp.message_handler(state=LevelStates.exercise)
async def process_exercise(message: types.Message, state: FSMContext):
    await LevelStates.next()
    await state.update_data(exercise_name=message.text)
    await message.answer('Введите номер уровня - число от 1 до 10')


@dp.message_handler(lambda message: not message.text.strip().isdigit() or
                    int(message.text.strip()) not in tuple(range(1, 11)),
                    state=LevelStates.level_num)
async def process_level_num_invalid(message: types.Message):
    return await message.answer('Номер уровня должен быть числом от 1 до 10')


@dp.message_handler(state=LevelStates.level_num)
async def process_level_num(message: types.Message, state: FSMContext):
    await LevelStates.next()
    await state.update_data(level_num=message.text)
    async with state.proxy() as data:
        level = Level.level_for_exercise(exercise_name=data['exercise_name'],
                                         level_num=data['level_num'])
        answer_message = Level.get_formatted_level(level)
        await message.answer(answer_message, parse_mode='HTML')
    await state.finish()


@dp.message_handler()
async def echo_message(message: types.Message):
    await message.answer('Попробуй набрать эту команду - /help')
