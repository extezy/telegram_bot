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

# ссылки на страницу с отелем не нашел в ответах от  API
# TODO формируется самостоятельно из id полученного отеля

# если произойдёт сценарий (/lowprice -> Введите город -> /highprice) то каким образом необходимо обрабатывать подобные случаи?
# TODO не допускать такого сценария, при переходе на другую команду спрашивать об этот обнулять ввод данных ранее введенных


# Интересует правлиьная структура проекта, где принято хранить файл БД, где обработчики событий типа файла /parsers/parser.py ?
# TODO в database


# Правильно ли реализована логика создания БД и таблиц в них, либо есть лучшее решение?
# TODO для данного проекта все верно


# Не понятен смысл использования файлов типа __init__: рассмотрим на примере keyboards -> inline, reply, __init__.py текущего проекта
# если внутри пакета reply прописано "from . import start_markup" и в основном файле каталога keyboards "from . import reply" то почему нельзя произвести импорт from keyboards import start_markup

# TODO все файлы init мы используем как некое хранилище для запуска инпутов чтобы не писать большую их часть в коде
# TODO на примере выше можно написать так как вы предложили

# Вопрос логирования: Можно ли оборачивать целиком обработчики событий, и на сколько это правильно:
# TODO нужно понимать что есть мы используем @logger.catch в некоторых случаях он можен залогировать конфендициальные данные
# TODO с которыми функция может упасть

"""
@logger.catch
@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
"""