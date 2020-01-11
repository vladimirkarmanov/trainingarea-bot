from aiogram import Dispatcher, executor

from app import dp
from views import (send_welcome, exercises_list,
                   cancel_handler, process_get_level,
                   process_exercise, process_level_num,
                   process_add_training, process_date,
                   process_exercise_repetitions, training_by_date,
                   trainings_list, unknown_command)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown)
