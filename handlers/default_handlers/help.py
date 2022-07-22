from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot
from loguru import logger


@bot.message_handler(commands=['help'])
def bot_help(message: Message) -> None:
    """
    Обработчик комманды бота "/help"
    выводит список и краткое описание доступных комманд бота
    :param message: сообщение с коммандой
    """
    logger.info(f"User_id: {message.from_user.id} use /help command")
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, '\n'.join(text))
