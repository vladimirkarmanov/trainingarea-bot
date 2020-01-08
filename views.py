import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from app import dp
from models.exercise import Exercise
from models.level import Level
from states import LevelStates
from utils import exceptions
from utils.validator import Validator
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
    await message.answer('Отмена операции')


@dp.message_handler(commands=['level'])
async def process_get_level(message: types.Message, state: FSMContext):
    await LevelStates.exercise.set()
    await message.answer('Введите название упражнения для '
                         'которого вы хотите посмотреть уровень')


@dp.message_handler(state=LevelStates.exercise)
async def process_exercise(message: types.Message, state: FSMContext):
    try:
        Validator.validate_exercise(message.text)
    except exceptions.NotCorrectMessage as e:
        logging.info(f'Raised "{str(e)}". Received msg: {message.text}')
        return await message.answer(str(e))

    await LevelStates.next()
    await state.update_data(exercise_name=message.text)
    await message.answer('Введите номер уровня - число от 1 до 10')


@dp.message_handler(state=LevelStates.level_num)
async def process_level_num(message: types.Message, state: FSMContext):
    try:
        Validator.validate_level(message.text)
    except exceptions.NotCorrectMessage as e:
        logging.info(f'Raised "{str(e)}". Received msg: {message.text}')
        return await message.answer(str(e))

    await LevelStates.next()
    await state.update_data(level_num=message.text)
    async with state.proxy() as data:
        level = Level.level_for_exercise(exercise_name=data['exercise_name'],
                                         level_num=data['level_num'])
        answer_message = Level.get_formatted_level(level)
        await message.answer(answer_message, parse_mode='HTML')
    await state.finish()


@dp.message_handler()
async def unknown_command(message: types.Message):
    await message.answer('Попробуй эту команду - /help')
