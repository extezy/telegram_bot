from peewee import Model

from loader import database

class BaseModel(Model):
    """
    Базовый класс для создания моделей
    """
    class Meta:
        database = database
