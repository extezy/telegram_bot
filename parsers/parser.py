from datetime import datetime
from datetime import timedelta
from config_data.config import MAX_HOTELS_COUNT
from config_data.config import MAX_PHOTO_COUNT
import requests
from config_data.config import RAPID_API_KEY
import re
from entities.city import City
from entities.hotel import Hotel
from loguru import logger


@logger.catch
def request_to_api(url, querystring) -> str:
    """
    Функция для запроса к API
    :param url: Строка для запроса
    :param querystring: Параметры
    :return: Ответ от сервера
    :rtype: str
    """

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        if response.status_code == requests.codes.ok:
            return response.text
    except Exception as exception:
        logger.error(f"Request  with url:{url}, querystring:{querystring} got: {exception}")


@logger.catch
def get_info_about_city(city_name: str, locale: str) -> list[City]:
    """
    Функция поиска  города по названию
    
    :param city_name: Название города
    :param locale: Указываем локацию  (ru_RU, en_US и т.д.)
    :return: Список каждый элемент которого является описанием найденного города 
     и содержит  словарь вида: 
                            "city_name": название города,  
                            "destinationid":Id города в базе сайта,
                            "caption": Описание города
    :rtype: list[dict]
    """

    city_group_parser = re.compile(r'((?<="CITY_GROUP",).*?])')  # ((?<="CITY_GROUP",).*?])   (?<="CITY_GROUP",).*?(?=])
    cities_parser = re.compile(r'((?={).*?CITY.*?})')  # Выделяем города
    city_destination_parser = re.compile(r'((?<="destinationId":").\d+)')  # Находим  destinationId города
    city_name_parser = re.compile(r'((?<="name":").*?(?="))')  # Находим название города   ((?<="name":").*?(?="))
    city_caption_parser = re.compile(r'((?<="caption":")\D*?(?="))')  # Находим описание ((?<="caption":")\D*?(?=",))   ((?<="caption":")+\D.*(?=",))
    city_clear_caption_parser = re.compile(r'([<].*?[>])')  # Чистим описание от лишнего

    result_cities = []

    url = "https://hotels4.p.rapidapi.com/locations/v2/search"

    querystring = {"query": city_name, "locale": locale, "currency": "USD"}

    response_text = request_to_api(url=url, querystring=querystring)

    if response_text is None:
        logger.info(f"Нулевой результат по городу от запроса: url={url}; querystring={querystring}")
        return result_cities

    city_group = city_group_parser.findall(response_text)
    if city_group:
        cities = cities_parser.findall(city_group[0])
        if len(cities) >= 1:
            for city in cities:
                new_city = None
                destinationid = city_destination_parser.findall(city)
                city_name = city_name_parser.findall(city)
                caption = city_caption_parser.findall(city)
                clear_caption = None
                if caption:
                    clear_caption = re.sub(city_clear_caption_parser, repl='', string=caption[0])

                if city_name:
                    new_city = City(str(city_name[0]))
                if destinationid:
                    new_city.id = str(destinationid[0])
                new_city.caption = clear_caption

                result_cities.append(new_city)

    return result_cities


@logger.catch
def get_info_about_hotels(destinationid: int,
                          locale: str,
                          price_highest_first: bool = None,
                          distance_range: str = None,
                          price_range: str = None,
                          page_number: int = 1,
                          pagesize: str = str(MAX_HOTELS_COUNT),
                          count_hotels_for_distance: int = None,
                          checkin: str = str(datetime.now().date()),
                          checkout: str = str(datetime.now().date() + timedelta(days=5))
                          ) -> list[Hotel]:

    """
    Функция поиска отелей по заданным  параметрам


    :param destinationid: ID города назначения
    :param locale: Локаль в  виде "ru_RU", "en_US" и т.д.
    :param price_highest_first: Параметр сортировки  по  цене:    True - дорогие,  False - дешевые, None - без сортировки.
    :param distance_range: Расстояние до центра в km в виде "5-15"
    :param price_range: Ценовой диапазон USD в виде "50-100"
    :param page_number: Номер страницы для запроса
    :param pagesize: Количество найденных отелей на одной странице
    :param count_hotels_for_distance: Количество отелей необходимых для поиска по  заданному расстоянию
    :param checkin: Дата заезда
    :param checkout: Дата отъезда
    :return: Список найденных отелей
    """

    url = "https://hotels4.p.rapidapi.com/properties/list"

    total_results_parser = re.compile(
        r'((?<="results":).+(?="pagination"))')  # Ищем все  полученные результаты на странице

    hotels_info_parser = re.compile(
        r'((?="id":).*?"features")')  # Ищем необходимые данные об отеле  включающие id и данные до центра  и  цены

    hotel_id_parser = re.compile(r'((?<="id":)\d*)')  # Получаем id отеля из hotels_info_parser

    hotel_name_parser = re.compile(r'((?<="name":").+?(?="))')  # Получаем название из отеля  hotels_info_parser

    hotel_street_parser = re.compile(
        r'((?<="streetAddress":").+?(?="))')  # Получаем улицу отеля из hotels_info_parser

    hotel_center_distance_parser = re.compile(
        r'((?<="City center","distance":").*?(?=[\s,]))')  # Получаем расстояние отеля от центра города ((?<="City center","distance":").*?[^\d].?\d) ((?<="City center","distance":").*?(?= miles"))

    hotel_price_per_night_parser = re.compile(
        r'((?<="exactCurrent":).*?(?=[\s,}]))')  # Получаем текущую стоимость комнаты за ночь  ((?<="exactCurrent":).*\d)     ((?<="exactCurrent":).*?(?=,))  ((?<="exactCurrent":).*?[^\d].?\d)

    hotel_price_total_parser = re.compile(
        r'((?<=total [$]).\d.*?(?=[\s,}]))')

    current_page_parser = re.compile(
        r'((?<="currentPage":)\d)')  # Текущая страница

    next_page_parser = re.compile(
        r'((?<="nextPageNumber":)\d)')  # Следующая страница

    querystring = ""

    distances = None

    nights_in_hotel = (datetime.strptime(checkout, "%Y-%m-%d") - datetime.strptime(checkin, "%Y-%m-%d")).days

    if price_range and distance_range:

        distances = distance_range.split('-')
        distances[0] = str(float(distances[0])*0.621)
        distances[1] = str(float(distances[1])*0.621)

        prices = price_range.split('-')
        querystring = {"destinationId": destinationid,
                       "pageNumber": page_number,
                       "pageSize": int(pagesize)*2,
                       "checkIn": checkin,
                       "checkOut": checkout,
                       "adults1": "1",
                       "priceMin": prices[0],
                       "priceMax": prices[1],
                       "locale": locale,
                       "currency": "USD"}

    elif price_highest_first is not None:

        querystring = {"destinationId": destinationid,
                       "pageNumber": "1",
                       "pageSize": pagesize,
                       "checkIn": checkin,
                       "checkOut": checkout,
                       "adults1": "1",
                       "sortOrder": "PRICE_HIGHEST_FIRST" if price_highest_first else "PRICE",
                       "locale": locale,
                       "currency": "USD"}

    result_hotels = []

    response_text = request_to_api(url=url, querystring=querystring)

    if response_text is None:
        logger.info(f"Нулевой результат по отелям от запроса: url={url}; querystring={querystring}")
        return result_hotels

    search_results = total_results_parser.findall(response_text)
    if search_results:
        full_hotels_info = hotels_info_parser.findall(search_results[0])

        # Запоминаем всё что нашло на первой странице в результат
        for hotel_info in full_hotels_info:
            hotel_id = hotel_id_parser.findall(hotel_info)
            hotel_name = hotel_name_parser.findall(hotel_info)
            hotel_street = hotel_street_parser.findall(hotel_info)
            hotel_center_distance = hotel_center_distance_parser.findall(hotel_info)
            hotel_price_per_night = hotel_price_per_night_parser.findall(hotel_info)
            hotel_price_total = hotel_price_total_parser.findall(hotel_info)

            new_hotel = Hotel(hotel_name[0])
            new_hotel.days_in_hotel = nights_in_hotel
            if hotel_id:
                new_hotel.id = str(hotel_id[0])
            if hotel_street:
                new_hotel.street = str(hotel_street[0])
            if hotel_center_distance:
                new_hotel.distance_to_center = float(hotel_center_distance[0])
            if hotel_price_per_night:
                new_hotel.cost_per_night = float(hotel_price_per_night[0])
            if hotel_price_total:
                new_hotel.price_per_stay = int(hotel_price_total[0])

            if distances:
                if type(new_hotel.distance_to_center) == float:
                    if float(distances[0]) <= new_hotel.distance_to_center <= float(distances[1]):
                        result_hotels.append(new_hotel)
                        count_hotels_for_distance -= 1
                        if count_hotels_for_distance == 0:
                            return result_hotels
            else:
                result_hotels.append(new_hotel)

        if count_hotels_for_distance and count_hotels_for_distance > 0:
            current_page = current_page_parser.findall(response_text)
            next_page = next_page_parser.findall(response_text)
            if next_page:
                if next_page[0] > current_page[0]:
                    hotels = get_info_about_hotels(destinationid=destinationid,
                                                   locale=locale,
                                                   price_highest_first=price_highest_first,
                                                   page_number=int(next_page[0]),
                                                   pagesize=pagesize,
                                                   price_range=price_range,
                                                   distance_range=distance_range,
                                                   count_hotels_for_distance=count_hotels_for_distance,
                                                   checkin=checkin,
                                                   checkout=checkout
                                                   )
                    result_hotels += hotels

    return result_hotels


@logger.catch
def get_hotel_photo(hotel: Hotel, photo_count: int = MAX_PHOTO_COUNT) -> Hotel:

    """
    Функция поиска фотографий отеля

    :param hotel: Отель для поиска фотографий
    :param photo_count: Количество необходимых фотографий
    :return: Отель с фотографиями
    :rtype: Hotel
    """

    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"id": hotel.id}

    total_urls_parser = re.compile(r'((?<="baseUrl":").*?(?="))') # Получаем все url фоток отеля
    clear_url_parser = re.compile(r'(_{size})')   # Получаем нужный (чистый) url для просмотра

    response_text = request_to_api(url=url, querystring=querystring)

    if response_text is None:
        logger.info(f"Нулевой результат по фото от запроса: url={url}; querystring={querystring}")
        return hotel

    total_urls = total_urls_parser.findall(response_text)

    count = 0
    if total_urls:
        for url_item in total_urls:
            clear_url = re.sub(clear_url_parser, repl='', string=url_item)
            if clear_url:
                if count >= photo_count:
                    return hotel
                hotel.photos = clear_url
                count += 1

    return hotel
