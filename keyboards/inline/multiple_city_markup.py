from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from entities.city import City


def get_city_keyboard(cities: list[City]) -> InlineKeyboardMarkup:
    """
    Функция для получения шаблона выбора города
    :return: набор кнопок с коммандами
    """
    approve_markup = InlineKeyboardMarkup(row_width=1)
    for city in cities:
        approve_markup.add(InlineKeyboardButton(text=f'{city.name} ({city.caption})', callback_data=f'id:{city.id}'))
    return approve_markup
