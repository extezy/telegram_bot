from telebot.types import Message
from loader import bot
from states.request_information import RequestInfoState
from loguru import logger


@bot.message_handler(commands=['highprice'])
def bot_start(message: Message):
    """
    Обработчик комманды бота "/highprice"
    сохраняет значение комманды в значение поля состояния "command"
    и переводит бот в состояние "city"
    :param message: сообщение с коммандой
    """
    logger.info(f"User_id: {message.from_user.id} use /highprice command")
    bot.set_state(message.from_user.id, RequestInfoState.city, message.chat.id)
    bot.send_message(message.from_user.id, f"Ищем самые дорогие отели. Введите город:")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as request:
        request['command'] = 'highprice'
