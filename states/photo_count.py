from telebot.types import Message
from loader import bot
from states.request_information import RequestInfoState
from config_data.config import MAX_PHOTO_COUNT
from keyboards.inline.request_approve_markup import get_data_approve_keyboard
from loguru import logger


@bot.message_handler(state=RequestInfoState.photo_count)
def get_photo_count(message: Message) -> None:
    """
    Обработчик состояния "photo_count"
    состояние для ввода количества фотографий при необходимости
    после чего запрашивает правильность полученных данных о запросе

    :param message: Строка с диапазоном
    """
    logger.info(f"User_id: {message.from_user.id} use photo_count state with message: {message.text}")
    if message.text.isnumeric():
        if 0 < int(message.text) <= MAX_PHOTO_COUNT:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as request:
                bot.send_message(message.from_user.id, 'Принято!')
                request['photo_count'] = message.text

                if request.get('command') == 'bestdeal':
                    result_request = f'Город: {request.get("city").name}\nЦена: {request.get("price")}\nРасстояние: {request.get("distance")}\nДаты: {request.get("start_date"):%d.%m.%Y} - {request.get("end_date"):%d.%m.%Y}\nКол-во отелей: {request.get("hotels_count")}\nКол-во фото: {request.get("photo_count")}'
                else:
                    result_request = f'Город: {request.get("city").name}\nДаты: {request.get("start_date"):%d.%m.%Y}-{request.get("end_date"):%d.%m.%Y}\nКол-во отелей: {request.get("hotels_count")}\nКол-во фото: {request.get("photo_count")}'

                bot.send_message(message.from_user.id, text=f'{result_request}\nДанные верны?',
                                 reply_markup=get_data_approve_keyboard())

    else:
        bot.send_message(message.from_user.id, f'минимум:1 максимум:{MAX_PHOTO_COUNT}')
