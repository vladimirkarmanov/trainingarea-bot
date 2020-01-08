import logging
import os

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import Config
from middlewares import AccessMiddleware

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s]    %(message)s'
)

PROXY_AUTH = aiohttp.BasicAuth(
    login=Config.TELEGRAM_PROXY_LOGIN,
    password=Config.TELEGRAM_PROXY_PASSWORD
)

bot = Bot(token=Config.API_TOKEN,
          proxy=Config.TELEGRAM_PROXY_URL,
          proxy_auth=PROXY_AUTH)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(AccessMiddleware(Config.ACCESS_ID))
