from telegram.ext import Updater

from bot.hendlers import start_handler, message_handler

updater = Updater(token='5142885956:AAHeMaBgQmeBedljCpI0qgGHlY8f6wzkuIY', use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()