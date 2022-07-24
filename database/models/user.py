from peewee import IntegerField, CharField, DateTimeField
from .base import BaseModel


class User(BaseModel):
    """
    Класс-модель для работы с БД
    используется для хранения информации о пользователях
    наследуется от BaseModel

    id: идентификатор в таблице, является primary_key
    first_name: телеграмм-first_name пользователя
    last_name: телеграмм-last_name пользователя
    user_id: телеграмм-ID пользователя
    username: телеграмм-username пользователя
    create_date: дата и время внесения пользователя в БД
    """
    id = IntegerField(primary_key=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    user_id = IntegerField()
    username = CharField(null=True)
    create_date = DateTimeField()

    class Meta:
        table_name = 'users'
