from telebot.types import Message
from loader import bot
from database.services.history import get_all_history
import pickle
from loguru import logger


@bot.message_handler(commands=['history'])
def bot_start(message: Message) -> None:
    """
    Обработчик комманды бота "/history"
    выводит историю запросов пользователя
    :param message: сообщение с коммандой
    """
    logger.info(f"User_id: {message.from_user.id} use /history command")
    history_results = get_all_history(message.from_user.id)
    bot.send_message(message.from_user.id, f'История ваших запросов:')
    for counter, value in enumerate(history_results):
        bot.send_message(message.from_user.id, f'*Дата и время запроса*:{value.get("date_time"):%Y-%m-%d %H:%M}', parse_mode="Markdown")
        history_message = f'{counter + 1}. {value.get("request_info")}\n'
        response = pickle.loads(value.get("response_info"))
        history_message += f'Полученные результаты:\n'
        bot.send_message(message.from_user.id, history_message)
        for item in response:
            if type(item) == str:
                bot.send_message(message.from_user.id, f'{item}')
            else:
                bot.send_media_group(message.chat.id, item)

    bot.send_message(message.from_user.id, "Готово. Чем еще могу помочь?")
