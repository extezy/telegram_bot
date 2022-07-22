from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config
from peewee import SqliteDatabase
from telebot_calendar import Calendar, RUSSIAN_LANGUAGE, CallbackData


storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
database = SqliteDatabase(config.DATABASE)
calendar_in_message = Calendar(language=RUSSIAN_LANGUAGE)
