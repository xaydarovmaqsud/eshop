from telegram import ReplyKeyboardMarkup
from bot.api import get_categories

main_markup = ReplyKeyboardMarkup(
    [
        [c['name']]
        for c in get_categories()
    ],
    resize_keyboard=True
)

categories_markup = ReplyKeyboardMarkup(
    [['Kategoriyalar','Savatcha'],
     ['Sayga o\'tish','Logout'],
     ['Orqaga']],
    resize_keyboard=True
)