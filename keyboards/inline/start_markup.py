from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Альтернативное меню для комманд
start_markup = InlineKeyboardMarkup( row_width=1)

help = InlineKeyboardButton(text='/help', callback_data='help')
lowprice = InlineKeyboardButton(text='/lowprice', callback_data='lowprice')
highprice = InlineKeyboardButton(text='/highprice', callback_data='highprice')
bestdeal = InlineKeyboardButton(text='/bestdeal', callback_data='bestdeal')
history = InlineKeyboardButton(text='/history', callback_data='history')

start_markup.add(lowprice, highprice, bestdeal, history, help)

def get_startup_markup() -> InlineKeyboardMarkup:
    """
    Функция для получения шаблона комманд бота
    :return: набор кнопок с коммандами
    """
    return start_markup