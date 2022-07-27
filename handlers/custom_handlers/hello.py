from telebot.types import Message
from loader import bot


@bot.message_handler(content_types=['text'])
def bot_hello(message: Message):
    """
    Обработчик текстовых сообщений, реагирует на приветствие на  русском языке в любом регистре: "Привет"
    :param message: текст сообщения
    """
    if message.text.lower() == 'привет':
        bot.reply_to(message, f'Привет, {message.from_user.full_name}!')
    else:
        bot.reply_to(message, f'Чтобы узнать что я умею наберите /help')
