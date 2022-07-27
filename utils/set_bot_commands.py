from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot):
    """
    Функция для добавления комманд для бота

    :param bot: Ссылка на бота
    """
    bot.set_my_commands(
        [BotCommand(*command) for command in DEFAULT_COMMANDS]
    )
