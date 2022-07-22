from telebot.types import Message
from keyboards.reply.start_markup import get_start_keyboard
from loader import bot
from states.request_information import RequestInfoState
from langdetect import detect
from parsers.parser import get_info_about_city
from keyboards.inline.multiple_city_markup import get_city_keyboard
from datetime import datetime
from loader import calendar_in_message
from loguru import logger


@bot.message_handler(state=RequestInfoState.city)
def get_city(message: Message) -> None:
    """
    Обработчик состояния "city"
    состояние для ввода города и поиска
    если нашло одно совпадение предлагает ввести даты заезда
    если несколько совпадений то предлагает выбрать  вариант из найденных

    :param message: Строка с диапазоном
    """
    logger.info(f"User_id: {message.from_user.id} use city state with message: {message.text}")
    if message.text.isprintable():
        bot.send_message(message.from_user.id, 'Ищу по городу...')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as request:

            if detect(message.text) == 'ru':
                locale = "ru_RU"
            else:
                locale = "en_US"

            request['locale'] = locale
            cities = get_info_about_city(city_name=message.text, locale=locale)

            if len(cities) > 1:
                # Несколько совпадений города
                request['cities'] = cities
                city_keyboard_markup = get_city_keyboard(cities)
                bot.send_message(message.from_user.id,
                                 'Уточните город:', reply_markup=city_keyboard_markup)
            elif len(cities) == 1:
                # Нашли единственное совпадение
                city = cities[0]
                bot.send_message(message.from_user.id, f'{city}')
                request['city'] = city
                bot.send_message(message.from_user.id, 'Выберите дату заезда',
                                 reply_markup=calendar_in_message.create_calendar('Дата', year=datetime.now().year,
                                                                                  month=datetime.now().month))
            else:
                bot.send_message(message.from_user.id, 'Активных отелей в городе не найдено',
                                 reply_markup=get_start_keyboard())
                bot.set_state(message.from_user.id, None, message.chat.id)
