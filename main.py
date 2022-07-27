from loader import bot
import handlers
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
from loguru import logger


if __name__ == '__main__':
    logger.add("./logs/work.log", format="{time} {level} {message}", level="DEBUG", rotation="50 MB", compression="zip")
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    logger.info("Bot started!...")
    bot.infinity_polling(allowed_updates=True)
