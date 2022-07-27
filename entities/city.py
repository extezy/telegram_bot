class City:
    """
    Класс для представления информации о городу

    Args:
        name (str): Название города

    """
    def __init__(self, name: str):
        self.__name = name
        self.__id = None
        self.__caption = "Без описания"

    def __str__(self):
        info = f'Название: {self.name} (Описание: {self.caption})'
        return info

    @property
    def name(self) -> str:
        """
        :return: Возвращает  название города
        :rtype: str
        """
        return self.__name

    @name.setter
    def name(self, name):
        """
        Устанавливает название города
        :param name: название города
        """
        self.name = name

    @property
    def id(self):
        """
        :return: Возвращает ID города
        :rtype: str
        """
        return self.__id

    @id.setter
    def id(self, destinationid: str):
        """
        Устанавливает ID города
        :param destinationid: ID города
        """
        self.__id = destinationid

    @property
    def caption(self) -> str:
        """
        :return: Описание города
        :rtype: str
        """
        return self.__caption

    @caption.setter
    def caption(self, caption):
        """
        Устанавливает описание города если оно есть
        :param caption: Описание города
        """
        if caption:
            self.__caption = caption
