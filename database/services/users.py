from database.models import User
from telebot.types import Message
from datetime import datetime
from loader import database
from loguru import logger


@logger.catch
def get_or_create_user(message: Message):
    """
    Функция для получения либо создания пользователя в БД

    :return: Пользователя
    """
    user = get_user(message.from_user.id)
    if user is None:
        user = User.get_or_create(first_name=message.from_user.first_name, last_name=message.from_user.last_name,
                                  user_id=message.from_user.id, username=message.from_user.username,
                                  create_date=datetime.now())

    return user


@logger.catch
def get_user(user_id: int) -> User:
    """
    Функция для получения пользователя из БД

    :param user_id: User.user_id
    :return: Пользователя, None если не нашло
    """
    return User.get_or_none(User.user_id == user_id)


@logger.catch
def get_users() -> list[User]:
    """
    Функция для получения списка пользователей бота

    :return: Список пользователей
    """
    query = User.select().dicts().execute()
    return query


# Создает таблицу User если такой не было
if database.table_exists(User) is False:
    database.create_tables([User])
