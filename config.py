import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


class Config:
    API_TOKEN = os.getenv('API_TOKEN')
    TELEGRAM_PROXY_URL = os.getenv('TELEGRAM_PROXY_URL')
    TELEGRAM_PROXY_LOGIN = os.getenv('TELEGRAM_PROXY_LOGIN')
    TELEGRAM_PROXY_PASSWORD = os.getenv('TELEGRAM_PROXY_PASSWORD')
    ACCESS_ID = os.getenv('ACCESS_ID')
