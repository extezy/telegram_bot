from loader import bot
from states.request_information import RequestInfoState
from keyboards.reply.start_markup import get_start_keyboard
from keyboards.inline.request_approve_markup import get_data_approve_keyboard
from parsers.parser import get_info_about_hotels
from parsers.parser import get_hotel_photo
from database.services.history import set_history
from telebot.types import InputMediaPhoto
from loader import calendar_in_message
from datetime import datetime, timedelta
import calendar
from loguru import logger


@logger.catch
@bot.callback_query_handler(func=lambda query: query.data in ['photo_approve', 'photo_cancel'])
def photo_callback(query):
    """
    Обрабатывает  события "С фото" и "Без фото"
    Если "С фото"-'photo_approve' то переводит в состояние обработки ввода количества фото
    Если "Без фото"-'photo_cancel' то переводит в состояние подтверждения данных
    :param query: callback-данные
    """
    logger.info(f"User_id: {query.from_user.id} work with callback: {query.data}")
    if query.data == "photo_approve":
        with bot.retrieve_data(query.from_user.id, query.message.chat.id) as request:
            # Переходим для загрузки вместе с фоточками
            bot.set_state(query.from_user.id, state=RequestInfoState.photo_count, chat_id=query.message.chat.id)
            bot.send_message(query.message.chat.id, 'Введите кол-во фото для отображения:')

    # Обработчик события Без фото
    if query.data == "photo_cancel":
        with bot.retrieve_data(query.from_user.id, query.message.chat.id) as request:
            bot.send_message(query.from_user.id, 'Принято!')

            if request.get('command') == 'bestdeal':
                result_request = f'Город: {request.get("city").name}\n' \
                                 f'Даты: {request.get("start_date"):%d.%m.%Y}-{request.get("end_date"):%d.%m.%Y}\n' \
                                 f'Цена: {request.get("price")}\n' \
                                 f'Расстояние: {request.get("distance")}\n' \
                                 f'Кол-во отелей: {request.get("hotels_count")}'
            else:
                result_request = f'Город: {request.get("city").name}\n' \
                                 f'Кол-во отелей: {request.get("hotels_count")}\n' \
                                 f'Даты: {request.get("start_date"):%d.%m.%Y} - {request.get("end_date"):%d.%m.%Y}\n'

            bot.send_message(query.from_user.id, text=f'{result_request}\nДанные верны?',
                             reply_markup=get_data_approve_keyboard())


@logger.catch
@bot.callback_query_handler(func=lambda query: query.data == 'request_approve')
def data_approve_callback(query):
    """
    Обрабатывает событие подтверждения данных
    после вывода полученных данных сбрасывает бота в начальное состояние и чистит все введенные данные
    :param query: callback-данные
    """
    logger.info(f"User_id: {query.from_user.id} work with callback: {query.data}")
    with bot.retrieve_data(query.from_user.id, query.message.chat.id) as request:
        bot.send_message(query.from_user.id, 'Делаю запрос!...', reply_markup=get_start_keyboard())

        result_request = f'Запрос: {request.get("command")} Город: {request.get("city")} Кол-во отелей: {request.get("hotels_count")}'

        # Обработка команд high- и lowprice
        if request.get('command') == 'lowprice':
            price_highest = False
        elif request.get('command') == 'highprice':
            price_highest = True
        else:
            price_highest = None

        if request.get('command') == 'bestdeal':
            hotels = get_info_about_hotels(destinationid=request.get("city").id,
                                           locale=request.get('locale'),
                                           price_highest_first=price_highest,
                                           pagesize=request.get('hotels_count'),
                                           price_range=request.get('price'),
                                           distance_range=request.get('distance'),
                                           count_hotels_for_distance=int(request.get('hotels_count')),
                                           checkin=request.get('start_date').strftime("%Y-%m-%d"),
                                           checkout=request.get('end_date').strftime("%Y-%m-%d")
                                           )
            result_request += f' Цена(USD): {request.get("price")} Расстояние(km): {request.get("distance")}'
        else:
            hotels = get_info_about_hotels(destinationid=request.get("city").id,
                                           locale=request.get('locale'),
                                           price_highest_first=price_highest,
                                           pagesize=request.get('hotels_count'),
                                           checkin=request.get('start_date').strftime("%Y-%m-%d"),
                                           checkout=request.get('end_date').strftime("%Y-%m-%d")
                                           )

        photo_count = request.get('photo_count')
        if photo_count:
            result_request += f' Кол-во фото: {photo_count}'
            for hotel in hotels:
                get_hotel_photo(hotel=hotel, photo_count=int(photo_count))

        response_with_photo = []
        response_without_photo = []
        if len(hotels) > 0:
            bot.send_message(query.from_user.id, "Отели:\n")
            for count, hotel in enumerate(hotels):
                hotel_info = f'Отель {count + 1}: {hotel}\n'
                # Делаем запись информации без фото
                response_without_photo.append(hotel_info)
                if len(hotel.photos) > 0:
                    photos = []
                    caption = True
                    for photo in hotel.photos:
                        if caption:
                            photos.append(InputMediaPhoto(photo, caption=hotel_info))
                            caption = False
                        else:
                            photos.append(InputMediaPhoto(photo))
                    # Делаем запись информации с фото
                    response_with_photo.append(photos)
                    bot.send_media_group(query.message.chat.id, photos)  # Отправка вместе с фото
                else:
                    bot.send_message(query.from_user.id, hotel_info)
        else:
            response_without_photo.append("По заданным параметрам ничего не найдено")
            bot.send_message(query.from_user.id, "По заданным параметрам ничего не найдено")
        bot.send_message(query.from_user.id, "Чем ещё могу помочь?")

        # Пишем историю запросов/ответов
        if len(response_with_photo) > 0:
            set_history(query.from_user.id, result_request, response_with_photo)
        else:
            set_history(query.from_user.id, result_request, response_without_photo)

        request.clear()
        # bot.send_message(query.from_user.id, response)
        bot.set_state(query.from_user.id, None,
                      query.message.chat.id)


@logger.catch
@bot.callback_query_handler(func=lambda query: query.data == 'request_cancel')
def data_cancel_callback(query):
    """
    Обрабатывает событие отмены введенных данных
    Сбрасывает бота в начальное состояние и чистит все введенные данные
    :param query: callback-данные
    """
    logger.info(f"User_id: {query.from_user.id} work with callback: {query.data}")
    bot.set_state(query.from_user.id, state=RequestInfoState.photo_count, chat_id=query.message.chat.id)
    with bot.retrieve_data(query.from_user.id, query.message.chat.id) as request:
        bot.send_message(query.from_user.id, 'Попробуйте ещё', reply_markup=get_start_keyboard())
        bot.set_state(query.from_user.id, None,
                      query.message.chat.id)  # Почему работает только с явным указанием сброса состояния, иначе происходит зацикливание на событиях?
        request.clear()


@logger.catch
@bot.callback_query_handler(func=lambda query: query.data.split(':')[0] == 'id')
def multiple_cities_callback(query):
    """
    Обрабатывает событие выбора уточненного города
    :param query: callback-данные
    """
    logger.info(f"User_id: {query.from_user.id} work with callback: {query.data}")
    with bot.retrieve_data(query.from_user.id, query.message.chat.id) as request:
        cities = request.get('cities')
        for city in cities:
            if city.id == str(query.data).split(':')[1]:
                request['city'] = city
                if request.get('command') == 'bestdeal':
                    bot.send_message(query.from_user.id, 'Город запомнил. Выберите дату заезда',
                                     reply_markup=calendar_in_message.create_calendar('Дата',
                                                                                      year=datetime.now().year,
                                                                                      month=datetime.now().month))
                else:
                    bot.send_message(query.from_user.id, 'Город запомнил. Выберите дату заезда',
                                     reply_markup=calendar_in_message.create_calendar('Дата',
                                                                                      year=datetime.now().year,
                                                                                      month=datetime.now().month))


@logger.catch
@bot.callback_query_handler(func=lambda query: query.data.startswith('Дата'))
def calendar_callback(query):
    """
        Обрабатывает callback-данные календаря: дату заезда, дату отъезда
        :param query: callback-данные
        """
    logger.info(f"User_id: {query.from_user.id} work with callback: {query.data}")

    def change_month(date_value: datetime, plus: bool) -> datetime:

        days_in_month = calendar.monthrange(date_value.year, date_value.month)[1]
        if plus:
            next_date = current_date + timedelta(days=days_in_month)
            return next_date
        else:
            prev_date = current_date - timedelta(days=1)
            return prev_date

    with bot.retrieve_data(query.from_user.id, query.message.chat.id) as request:

        if request.get('start_date'):
            date_type = 'end'
        elif request.get('end_date'):
            date_type = None
        else:
            date_type = 'start'

        if date_type is False:
            bot.send_message(query.from_user.id, 'Случайно попали не туда, начнем с начала',
                             reply_markup=get_start_keyboard())
            request.clear()

        name, action, year, month, day = query.data.split(':')  #

        if action == "DAY":
            if date_type == 'start':
                # Запоминаем дату заезда
                start_date = datetime.strptime(f'{year}-{month}-{day}', "%Y-%m-%d")
                bot.send_message(query.from_user.id, f'Дата заезда: {start_date:%d.%m.%Y}')
                request['start_date'] = start_date
                # Переходим к выбору даты отъезда
                bot.send_message(query.from_user.id, 'Выберите дату отъезда',
                                 reply_markup=calendar_in_message.create_calendar('Дата', year=int(year),
                                                                                  month=int(month)))
            elif date_type == 'end':
                end_date = datetime.strptime(f'{year}-{month}-{day}', "%Y-%m-%d")

                # Проверяем валидность даты отъезда
                if end_date > request.get('start_date'):
                    # Запоминаем  дату отъезда
                    bot.send_message(query.from_user.id, f'Дата отъезда: {end_date:%d.%m.%Y}')
                    request['end_date'] = end_date
                    bot.set_state(query.from_user.id, RequestInfoState.hotels_count, query.message.chat.id)

                    # смотрим куда идти дальше
                    if request.get('command') == 'bestdeal':
                        bot.send_message(query.from_user.id,
                                         'Город запомнил. Введите две границы ценового диапазона разделенные дефисом(USD):')
                        bot.set_state(query.from_user.id, RequestInfoState.price, query.message.chat.id)
                    else:
                        bot.send_message(query.from_user.id,
                                         'Город запомнил. Введите кол-во отелей для отображения:')
                        bot.set_state(query.from_user.id, RequestInfoState.hotels_count, query.message.chat.id)
                else:
                    # Возвращаемся к выбору даты
                    bot.send_message(query.from_user.id,
                                     'Дата отъезда должна быть позже даты приезда!\nВыберите дату отъезда',
                                     reply_markup=calendar_in_message.create_calendar('Дата', year=int(year),
                                                                                      month=int(month)))

        elif action == "CANCEL":
            if date_type == 'end':
                request['start_date'] = None
                bot.send_message(query.from_user.id, 'Выберите дату заезда',
                                 reply_markup=calendar_in_message.create_calendar('Дата', year=int(year),
                                                                                  month=int(month)))
            else:
                bot.send_message(query.from_user.id, 'Начнем с начала. Что бы Вы хотели сделать?',
                                 reply_markup=get_start_keyboard())

        elif action == "NEXT-MONTH":
            current_date = datetime.strptime(f'{year}-{month}-1', "%Y-%m-%d")
            next_date = change_month(date_value=current_date, plus=True)
            bot.send_message(query.from_user.id, 'Следующий месяц',
                             reply_markup=calendar_in_message.create_calendar('Дата', year=next_date.year,
                                                                              month=next_date.month))

        elif action == "PREVIOUS-MONTH":
            current_date = datetime.strptime(f'{year}-{month}-1', "%Y-%m-%d")
            prev_date = change_month(date_value=current_date, plus=False)
            bot.send_message(query.from_user.id, 'Предыдущий месяц',
                             reply_markup=calendar_in_message.create_calendar('Дата', year=prev_date.year,
                                                                              month=prev_date.month))
