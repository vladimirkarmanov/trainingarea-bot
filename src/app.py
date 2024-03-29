import logging

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import Config

if Config.DEBUG:
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] [%(levelname)s]   %(message)s')
    PROXY_AUTH = aiohttp.BasicAuth(login=Config.TELEGRAM_PROXY_LOGIN,
                                   password=Config.TELEGRAM_PROXY_PASSWORD)
    bot = Bot(token=Config.TELEGRAM_API_TOKEN,
              proxy=Config.TELEGRAM_PROXY_URL,
              proxy_auth=PROXY_AUTH)
else:
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] [%(levelname)s]   %(message)s',
                        filename='log_bot.log')

    bot = Bot(token=Config.TELEGRAM_API_TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())
