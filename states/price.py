from telebot.types import Message
from loader import bot
from states.request_information import RequestInfoState
from loguru import logger


@bot.message_handler(state=RequestInfoState.price)
def get_price(message: Message) -> None:
    """
    Обработчик состояния "price"
    состояние для ввода диапазона цен
    после чего направляет на состояние "distance"

    :param message: Строка с диапазоном
    """
    logger.info(f"User_id: {message.from_user.id} use price state with message: {message.text}")
    prices = message.text.split('-')
    if len(prices) == 2 and prices[0].isnumeric() and prices[1].isnumeric():
        if prices[0] <= prices[1]:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as request:
                request['price'] = message.text
                bot.send_message(message.from_user.id, 'Цену запомнил. Введите диапазон расстояния через дефис(км):')
                bot.set_state(message.from_user.id, RequestInfoState.distance, message.chat.id)
        else:
            bot.send_message(message.from_user.id, 'Нижняя граница не может быть больше верхней!')
    else:
        bot.send_message(message.from_user.id, 'Введите две границы диапазона разделенные дефисом (10-90) USD')
