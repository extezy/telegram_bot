from telebot.types import Message
from loader import bot
from states.request_information import RequestInfoState
from loguru import logger


@bot.message_handler(state=RequestInfoState.distance)
def get_price(message: Message) -> None:
    """
    Обработчик состояния "distance"
    состояние для ввода диапазона расстояний
    после чего меняет состояние на "hotels_count"

    :param message: Строка с диапазоном
    """
    logger.info(f"User_id: {message.from_user.id} use distance state with message: {message.text}")
    distances = message.text.split('-')
    if len(distances) == 2 and distances[0].isnumeric() and distances[1].isnumeric():
        if distances[0] <= distances[1]:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as request:
                request['distance'] = message.text
                bot.send_message(message.from_user.id, 'Расстояние запомнил. Введите кол-во отелей для отображения:')
                bot.set_state(message.from_user.id, RequestInfoState.hotels_count, message.chat.id)
        else:
            bot.send_message(message.from_user.id, 'Нижняя граница не может быть больше верхней!')
    else:
        bot.send_message(message.from_user.id, 'Введите границы диапазона расстояния через дефис:(1000-1500) км!')
