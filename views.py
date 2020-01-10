import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import aiofiles

from app import dp
from models.exercise import Exercise
from models.exercise_repetitions import ExerciseRepetitions
from models.level import Level
from models.photo import Photo
from models.training import Training
from states import LevelStates, TrainingStates
from utils import exceptions
from utils.parser import Parser
from utils.validator import Validator


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    logging.info(f'Received command {message.get_command()}')
    await message.answer(
        'Бот для программы тренировок "Тренировочная зона"\n\n'
        'Показать упражнения: /exercises\n'
        'Показать уровень для упражнения: /level'
    )


@dp.message_handler(commands=['exercises'])
async def exercises_list(message: types.Message):
    exercises = Exercise.all()
    answer_message = Parser.list_objs_to_string(exercises)
    logging.info(f'Received command {message.get_command()},'
                 f' sending {answer_message}')
    await message.answer(answer_message)


@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info(f'Received command {message.get_command()}')
    logging.info(f'Cancelling state {current_state}')
    await state.finish()
    await message.answer('Отмена операции')


@dp.message_handler(commands=['level'])
async def process_get_level(message: types.Message):
    await LevelStates.exercise.set()
    logging.info(f'Received command {message.get_command()}')
    logging.info('Setting state LevelStates.exercise')
    await message.answer('Введите название упражнения для '
                         'которого вы хотите посмотреть уровень')


@dp.message_handler(state=LevelStates.exercise)
async def process_exercise(message: types.Message, state: FSMContext):
    try:
        exercise_name = Validator.clean_exercise(message.text)
    except exceptions.NotCorrectMessage as e:
        logging.error(f'Raised "{str(e)}". Received msg: {message.text}')
        return await message.answer(str(e))

    await LevelStates.next()
    await state.update_data(exercise_name=exercise_name)
    logging.info(f'Adding state data: {exercise_name}')
    logging.info(f'Setting state {await state.get_state()}')
    await message.answer('Введите номер уровня - число от 1 до 10')


@dp.message_handler(state=LevelStates.level_num)
async def process_level_num(message: types.Message, state: FSMContext):
    try:
        level_num = Validator.clean_level(message.text)
    except exceptions.NotCorrectMessage as e:
        logging.error(f'Raised "{str(e)}". Received msg: {message.text}')
        return await message.answer(str(e))

    async with state.proxy() as data:
        level = Level.level_for_exercise(exercise_name=data['exercise_name'],
                                         level_num=level_num)
        photos = Photo.get_photos_for_level(level.get('name'))
        caption = Level.get_formatted_level(level)
        logging.info(f'Sending caption: {caption}')
        await message.answer(caption, parse_mode='HTML')
        for photo in photos:
            async with aiofiles.open(photo, 'rb') as p:
                logging.info(f'Sending photo: {photo}')
                await message.answer_photo(p)
    logging.info(f'Finishing state LevelStates')
    await state.finish()


@dp.message_handler(commands=['add'])
async def process_add_training(message: types.Message):
    await TrainingStates.date.set()
    logging.info(f'Received command {message.get_command()}')
    logging.info('Setting state TrainingStates.date')
    await message.answer('Введите дату тренировки в формате YYYY-MM-DD')


@dp.message_handler(state=TrainingStates.date)
async def process_date(message: types.Message, state: FSMContext):
    try:
        date = Validator.clean_date(message.text)
    except exceptions.NotCorrectMessage as e:
        logging.error(f'Raised "{str(e)}". Received msg: {message.text}')
        return await message.answer(str(e))

    await TrainingStates.next()
    await state.update_data(date=date)
    logging.info(f'Adding state data: {date}')
    logging.info(f'Setting state {await state.get_state()}')
    await message.answer('Введите упражнения и повторы в формате:\n'
                         'упражнение1(7 уровень) - 15 20 10 12\n'
                         'упражнение2(4 уровень) - 50 55 48')


@dp.message_handler(state=TrainingStates.exercises_repetitions)
async def process_exercise_repetitions(message: types.Message,
                                       state: FSMContext):
    try:
        exercises_repetitions = Parser.parse_exercises_repetitions(
            message.text)
        for exercise, level, repetitions in exercises_repetitions:
            Validator.clean_exercise(exercise)
            Validator.clean_level(level)
            Validator.clean_repetitions(repetitions)
    except exceptions.NotCorrectMessage as e:
        logging.error(f'Raised "{str(e)}". Received msg: {message.text}')
        return await message.answer(str(e))

    async with state.proxy() as data:
        Training.add_training(data['date'])
        pk_training = Training.last()['id']
        for exercise, level, repetitions in exercises_repetitions:
            pk_level = Level.level_for_exercise(exercise, level)['name']
            ExerciseRepetitions.add_exercise_repetitions(int(pk_training),
                                                         exercise,
                                                         pk_level,
                                                         repetitions)
        logging.info('Adding training to database')
        await message.answer('Тренировка успешно добавлена')
    await state.finish()


@dp.message_handler(commands=['training'])
async def process_add_training(message: types.Message):
    logging.info(f'Received command {message.get_command()}')
    await message.answer('Введите дату тренировки в формате YYYY-MM-DD')


@dp.message_handler()
async def unknown_command(message: types.Message):
    logging.info(f'Received command {message.get_command()}')
    await message.answer('Попробуй эту команду - /help')
