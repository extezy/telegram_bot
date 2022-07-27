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
        self.__hotels_in_search_result = []

    def __str__(self):
        info = f'Название: {self.name} (Описание: {self.caption})'
        return info

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name):
        self.name = name

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, destinationid):
        self.__id = destinationid

    @property
    def caption(self) -> str:
        return self.__caption

    @caption.setter
    def caption(self, caption):
        if caption:
            self.__caption = caption

    @property
    def hotels_in_search_result(self) -> list:
        return self.__hotels_in_search_result


# TODO дописать докстринги

