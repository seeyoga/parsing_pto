import os

from loguru import logger
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_V3_API_KEY")


logger.add('parsing_pto.log', format='{time} {level} {message}', level='INFO', encoding="utf-8")  # Настройки логов
