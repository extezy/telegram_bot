from datetime import datetime
from database.models.history import History
from loader import database
import pickle
from loguru import logger


@logger.catch
def set_history(user_id, request_info: str, response_info: list) -> None:
    """
    Функция для записи запроса в БД

    :param user_id: телеграм-id пользователя
    :param request_info: информация о запросе
    :param response_info: найденный результат
    """
    response = pickle.dumps(response_info)
    History.get_or_create(user_id=user_id, date_time=datetime.now(), request_info=request_info,
                          response_info=response)


@logger.catch
def get_all_history(user_id: int) -> list:
    """
    Функция для получения списка всех запросов пользователя

    :param user_id: телеграм-ID пользователя
    :return: Список пользователей
    """
    query = History.select().where(History.user_id == user_id).order_by(History.date_time).dicts().execute()
    return list(query)


# Создает таблицу History если такой не было
if database.table_exists(History) is False:
    database.create_tables([History])
