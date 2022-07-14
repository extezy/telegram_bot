import os
import telebot

from handlers import history, lowprice, bestdeal, highprice

bot = telebot.TeleBot(os.environ.get('TeleBot'))

if __name__ == '__main__':

    @bot.message_handler(commands=['hello-world'])
    def send_welcome(message):
        bot.reply_to(message, f"Hello world!!! From, {message.from_user.first_name}!")

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.reply_to(message, "Howdy, how are you doing?")

    @bot.message_handler(commands=['lowprice'])
    def send_welcome(message):
        bot.reply_to(message, lowprice.get())

    @bot.message_handler(commands=['highprice'])
    def send_welcome(message):
        bot.reply_to(message, highprice.get())

    @bot.message_handler(commands=['bestdeal'])
    def send_welcome(message):
        bot.reply_to(message, bestdeal.get())

    @bot.message_handler(commands=['history'])
    def send_welcome(message):
        bot.reply_to(message, history.get())

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.text.lower() == 'привет':
            bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}!')


    bot.polling(none_stop=True, interval=0)
