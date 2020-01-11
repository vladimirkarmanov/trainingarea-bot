import os

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')


class Config:
    DEBUG = bool(int(os.getenv('DEBUG')))
    TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
    TELEGRAM_PROXY_URL = os.getenv('TELEGRAM_PROXY_URL')
    TELEGRAM_PROXY_LOGIN = os.getenv('TELEGRAM_PROXY_LOGIN')
    TELEGRAM_PROXY_PASSWORD = os.getenv('TELEGRAM_PROXY_PASSWORD')
    TELEGRAM_ACCESS_ID = os.getenv('TELEGRAM_ACCESS_ID')
    TIMEZONE = os.getenv('TZ')
