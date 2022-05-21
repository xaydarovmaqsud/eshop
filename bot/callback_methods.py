import json
import requests
from telegram import Update
from telegram.ext import CallbackContext
from redis_connection import redis_connection as redconn
from bot.inline_keyboards import products_keyboard
from bot.keyboards import main_markup, categories_markup
from bot.make_image import get_gr_photo
from api import bot_login, get_my_cart


def start(update: Update, context: CallbackContext):
    try:
        user_data = json.loads(redconn.get(f'{update.message.from_user.id}'))
        print('Mana data:\n',user_data)
    except:
        user_data=None
    if user_data and len(user_data)>2:
        token = user_data.get('token', None)
        if token:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Salom, bu bot ishga tushdi!",
                reply_markup=categories_markup
            )
    else:
        redconn.mset({f'{update.message.from_user.id}': json.dumps({})})
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Salom, bu bot ishga tu shdi!\n\nOnline do'konimizning imkoniyatlaridan to'liq foydalanishingiz uchun tizimga kirishingiz zarur\n\n❗Telefon kiriting:",
            # reply_markup={remove_keyboard:true }
        )


def message(update: Update, context: CallbackContext):
    message = update.message.text
    print('user id:', update.message.from_user.id)
    try:
        user_json = redconn.get(f'{update.message.from_user.id}')
        if user_json:
            data = {
                "phone_number": message,
            }
            user_data=json.loads(user_json)
            token = user_data.get('token', None)
            phone_number = user_data.get('phone_number', None)
            if token:
                if message == 'Kategoriyalar':
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Marhamat kerakli kategoriyani tanlang",
                        reply_markup=main_markup
                    )
                elif message == 'Savatcha':
                    res=get_my_cart()
                    print(res)
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"1.{res[0]}\n 2.{res[1]}\n 3.{res[2]}\n 4.{res[3]} ",
                        reply_markup=categories_markup
                    )
                elif message == 'Orqaga':
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"Bosh sahifa",
                        reply_markup=categories_markup
                    )
                else:
                    pkeyboard,keys = products_keyboard(message,page=1)
                    context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=open(get_gr_photo(keys),'rb'),
                        caption='Kerakli raqamni tanlang !',
                        reply_markup=pkeyboard
                    )
            elif phone_number:
                data['password']=message
                # Api request token
                response=bot_login(data)
                res_token = response.json()
                # End api
                if response.status_code==200:
                    redconn.mset({f'{update.message.from_user.id}': json.dumps({
                        'phone_number':phone_number,
                        'password':message,
                        'token': res_token['token'],
                    })})
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"✅🥳 Tabriklayman tizimga kirdiz!\n/start qayta bosing!!!",
                    )
                else:
                    redconn.mset({f'{update.message.from_user.id}': json.dumps({
                        'phone_number': phone_number,})})
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"🚫 Telefon raqam yoki parol xato! 🚫\n Qayta urinib kuring! /start",
                    )
                    redconn.delete(f'{update.message.from_user.id}')
            else:
                redconn.mset({f'{update.message.from_user.id}': json.dumps({
                    'phone_number': message,
                })})
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Password"
                )
        else:
            redconn.mset({f'{update.message.from_user.id}': json.dumps({})})
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Online do'konimizning imkoniyatlaridan to'liq foydalanishingiz uchun tizimga kirishingiz zarur /start"
            )
    except Exception as e:
        print("error:", e)
