from telebot.types import Message
from loader import bot
from states.request_information import RequestInfoState
from config_data.config import MAX_HOTELS_COUNT
from keyboards.inline.photo_approve_markup import get_photo_approve_keyboard
from loguru import logger


@bot.message_handler(state=RequestInfoState.hotels_count)
def get_hotels_count(message: Message) -> None:
    """
    Обработчик состояния "hotels_count"
    состояние для ввода количества отелей для отображения
    после чего запрашивает необходимость фотографий в ответе

    :param message: Строка с диапазоном
    """
    logger.info(f"User_id: {message.from_user.id} use hotels_count state with message: {message.text}")
    if message.text.isnumeric():
        if 0 < int(message.text) <= MAX_HOTELS_COUNT:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as request:
                request['hotels_count'] = message.text
            bot.send_message(message.from_user.id, 'Количество отелей запомнил. Необходимы ли фото отелей?',
                             reply_markup=get_photo_approve_keyboard())
        else:
            bot.send_message(message.from_user.id, f'минимум: 1, максимум: {MAX_HOTELS_COUNT}')
    else:
        bot.send_message(message.from_user.id, 'Необходимо ввести положительное число!')
