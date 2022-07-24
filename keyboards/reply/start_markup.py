from telebot.types import ReplyKeyboardMarkup, KeyboardButton


markup = ReplyKeyboardMarkup(True, True, row_width=4)

help = KeyboardButton(text='/help')
lowprice = KeyboardButton(text='/lowprice')
highprice = KeyboardButton(text='/highprice')
bestdeal = KeyboardButton(text='/bestdeal')
history = KeyboardButton(text='/history')

markup.add(lowprice, highprice, bestdeal, history, help)


def get_start_keyboard() -> ReplyKeyboardMarkup:
    """
    Функция для получения шаблона комманд бота
    :return: набор кнопок с коммандами
    """
    return markup
