class Hotel:
    """
    Класс для представления информации о отеле

    Args:
        name (str): Название отеля

    """
    def __init__(self, name: str):
        self.__name = name
        self.__id = None
        self.__street = "Без адреса"
        self.__distance_to_center = None
        self.__cost_per_night = None
        self.__days_in_hotel = None
        self.__price_per_stay = 0
        self.__photos = []

    def __str__(self):
        """
        :return: Выводит информацию о отеле
        """
        info = f'Название: {self.name}, Адрес:{self.street}, До центра: {self.distance_to_center} miles, Стоимость ночи: {self.__cost_per_night} USD, Полная стоимость: {self.price_per_stay} USD, {self.get_link()}'
        return info

    @property
    def name(self) -> str:
        """
        :return: Название отеля
        """
        return self.__name

    @name.setter
    def name(self, name: str):
        """
        Устанавливает название отеля
        :param name: Название отеля
        """
        if name.isalnum():
            self.__name = name

    @property
    def id(self) -> str:
        """
        :return: ID отеля
        """
        return self.__id

    @id.setter
    def id(self, hotel_id: str):
        """
        Устанавливает ID отеля
        :param hotel_id: ID отеля
        """
        self.__id = hotel_id

    @property
    def street(self) -> str:
        """
        :return: Адрес отеля
        """
        return self.__street

    @street.setter
    def street(self, street: str):
        """
        Устанавливает адрес отеля
        :param street: Адрес отеля
        """
        self.__street = street

    @property
    def distance_to_center(self):
        """
        :return: Расстояние от отеля до центра города
        :rtype: int если расстояние указано, и str с описанием иначе
        """
        if self.__distance_to_center:
            return self.__distance_to_center
        else:
            return 'Нет данных'

    @distance_to_center.setter
    def distance_to_center(self, distance: float):
        """
        Устанавливает расстрояние от отеля до центра города
        :param distance: расстояние до центра города
        """
        if distance > 0:
            self.__distance_to_center = distance
        else:
            self.__distance_to_center = 0

    @property
    def cost_per_night(self):
        """
        :return: Стоимость комнаты отеля за ночь
        :rtype: int если стоимость указана, str если нет указанной стоимости
        """
        if self.__cost_per_night != 0:
            return self.__cost_per_night
        else:
            return 'Нет данных'

    @cost_per_night.setter
    def cost_per_night(self, cost: float):
        """
        Устанавливает комнаты отеля за ночь
        :param cost: Стоимость комнаты
        """
        if cost > 0:
            self.__cost_per_night = cost
        else:
            self.__cost_per_night = 0

    @property
    def days_in_hotel(self):
        """
        :return: Планируемое количество ночей в отеле
        """
        if self.__days_in_hotel != 0:
            return self.__days_in_hotel
        else:
            return 0

    @days_in_hotel.setter
    def days_in_hotel(self, days: int):
        """
        Устанавливает значение
        :param days: Количество ночей в отеле
        :return:
        """
        if days > 0:
            self.__days_in_hotel = days
        else:
            self.__days_in_hotel = 0

    @property
    def price_per_stay(self):
        """
        :return: Стоимость проживания за указанный период
        """
        if self.__price_per_stay != 0:
            return self.__price_per_stay
        else:
            return 0

    @price_per_stay.setter
    def price_per_stay(self, price: int):
        """
        Устанавливает  стоимость проживания за указанный период
        :param price: Стоимость проживания
        """
        if price > 0:
            self.__price_per_stay = price
        else:
            self.__price_per_stay = 0

    @property
    def photos(self) -> list:
        """
        :return: URL фотографий отеля
        """
        return self.__photos

    @photos.setter
    def photos(self, photo_url: str):
        """
        Добавляет URL фотографии отеля
        :param photo_url: URL фотографии
        """
        self.__photos.append(photo_url)

    def get_link(self):
        """
        :return: Сформированная ссылка на отель
        """
        return f'https://www.hotels.com/ho{self.id}'
