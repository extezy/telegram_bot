import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

ROOT_DIR = os.path.dirname(os.path.abspath('__main__'))
BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DATABASE = os.path.join(ROOT_DIR, 'database', 'history.db')
MAX_HOTELS_COUNT = 10
MAX_PHOTO_COUNT = 10

DEFAULT_COMMANDS = (
    ('lowprice', "Топ дешевых отелей"),
    ('highprice', "Топ дорогих отелей"),
    ('bestdeal', "Топ подходящих отелей"),
    ('history', "История поиска"),
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
)
