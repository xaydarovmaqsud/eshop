from telegram import InlineKeyboardButton,InlineKeyboardMarkup

from bot.api import get_products,get_cat_id

def products_keyboard(category,page=1):
    datas = get_products(get_cat_id(category),page=1)
    keys = [data['id'] for data in datas]
    return InlineKeyboardMarkup([
    [InlineKeyboardButton(data['name'], callback_data=data['id'])]
    for data in datas
    ]),keys