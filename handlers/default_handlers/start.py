from telebot.types import Message
from database.services import users
from loader import bot
from keyboards.reply.start_markup import get_start_keyboard
from loguru import logger


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    """
    Обработчик комманды бота "/start"
    приветствует пользователя и предлагает ему выбрать действия из меню
    :param message: сообщение с коммандой
    """
    logger.info(f"User_id: {message.from_user.id} use /start command")
    users.get_or_create_user(message)
    bot.reply_to(message, f"Добро пожаловать, {message.from_user.full_name}!")
    bot.send_message(message.from_user.id, 'Что бы Вы хотели сделать?', reply_markup=get_start_keyboard())
