from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


approve_markup = InlineKeyboardMarkup(row_width=2)

yes = InlineKeyboardButton(text='Да', callback_data='request_approve')
no = InlineKeyboardButton(text='Нет', callback_data='request_cancel')
approve_markup.add(yes, no)


def get_data_approve_keyboard() -> InlineKeyboardMarkup:
    """
    Функция для получения шаблона для подтверждения правильности введенных данных
    :return: набор кнопок с коммандами
    """
    return approve_markup
