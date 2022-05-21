

from telegram.ext import CommandHandler, MessageHandler, Filters

from bot.callback_methods import start,message

start_handler = CommandHandler('start', start)
message_handler=MessageHandler(Filters.text | Filters.photo,message)
