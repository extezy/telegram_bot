from telebot.handler_backends import State, StatesGroup


class RequestInfoState(StatesGroup):
    """
    Класс для хранения состояний бота
    """
    city = State()
    hotels_count = State()
    photo = State()
    photo_count = State()
    price = State()
    distance = State()
    request_data = State()
