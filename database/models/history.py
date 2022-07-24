from peewee import CharField, DateTimeField, ForeignKeyField, IntegerField, BlobField
from .base import BaseModel
from .user import User


class History(BaseModel):
    """
    Класс-модель для работы с БД
    используется для хранения истории запросов
    наследуется от BaseModel

    id: идентификатор в таблице, является primary_key
    user_id: телеграмм-ID пользователя
    date_time: дата и время запроса
    request_info: информация о запросе
    response_info: полученный результат
    """
    id = IntegerField(primary_key=True)
    user_id = ForeignKeyField(User, 'user_id')
    date_time = DateTimeField()
    request_info = CharField()
    response_info = BlobField()

    class Meta:
        table_name = 'history'
