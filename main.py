from loader import bot
import handlers
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
from loguru import logger


if __name__ == '__main__':
    logger.add("./logs/work.log", format="{time} {level} {message}", level="DEBUG", rotation="50 MB", compression="zip")
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    logger.info("Bot started!...")
    try:
        bot.infinity_polling()
    except Exception as exeption:
        logger.error(exeption)

# TODO ссылки на страницу с отелем не нашел в ответах от  API

# TODO если произойдёт сценарий (/lowprice -> Введите город -> /highprice) то каким образом необходимо обрабатывать подобные случаи?

# TODO Интересует правлиьная структура проекта, где принято хранить файл БД, где обработчики событий типа файла /parsers/parser.py ?

# TODO Правильно ли реализована логика создания БД и таблиц в них, либо есть лучшее решение?

# TODO  Не понятен смысл использования файлов типа __init__: рассмотрим на примере keyboards -> inline, reply, __init__.py текущего проекта
# TODO  если внутри пакета reply прописано "from . import start_markup" и в основном файле каталога keyboards "from . import reply" то почему нельзя произвести импорт from keyboards import start_markup

# TODO Вопрос логирования: Можно ли оборачивать целиком обработчики событий, и на сколько это правильно:
"""
@logger.catch
@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
"""