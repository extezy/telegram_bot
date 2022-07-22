from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


approve_markup = InlineKeyboardMarkup(row_width=2)

yes = InlineKeyboardButton(text='Да', callback_data='photo_approve')
no = InlineKeyboardButton(text='Нет', callback_data='photo_cancel')
approve_markup.add(yes, no)


def get_photo_approve_keyboard() -> InlineKeyboardMarkup:
    """
    Функция для получения шаблона для выбора сценария поиска с фото или без
    :return: набор кнопок с коммандами
    """
    return approve_markup
