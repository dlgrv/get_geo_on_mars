from config import token
import emoji
import telebot
from telebot import types
from photo_generator import photo_generator
import db
import keybaord
import text_

bot = telebot.TeleBot(token)

def save_user_profile_photo(message):
    profile_photo_file_id = bot.get_user_profile_photos(message.chat.id).photos
    if profile_photo_file_id != []:
        try:
            profile_photo_file_id = profile_photo_file_id[0][-1].file_id
            file_info = bot.get_file(profile_photo_file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            img_name = message.chat.id
            src = f'./users_profile_photos/{img_name}.jpg'
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
        except Exception as e:
            print('Error from save_user_profile_photo: ', e)

@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        check_user = db.check_user(message.from_user.id)
        if check_user:
            # НЕ В ПЕРВЫЙ РАЗ
            bot.send_message(message.chat.id,
                             text=text_.repeat_start(),
                             reply_markup=keybaord.lang())
            save_user_profile_photo(message)
        else:
            # В ПЕРВЫЙ РАЗ
            bot.send_message(message.chat.id,
                             text=text_.first_start(),
                             reply_markup=keybaord.lang())
            db.add_user(message.from_user.id, message.from_user.username)
            save_user_profile_photo(message)
    except Exception as e:
        print(e)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.delete_message(call.from_user.id, call.message.id)
    if call.data == 'rus':
        bot.answer_callback_query(call.id, f'Язык выбран{emoji.CHECK_MARK_BUTTON}')
        bot.send_message(call.from_user.id,
                         text=text_.instruction('rus'),
                         reply_markup=keybaord.menu('rus'))
        db.update_language(call.from_user.id, 'rus')
    elif call.data == 'eng':
        bot.answer_callback_query(call.id, f'Language selected{emoji.CHECK_MARK_BUTTON}')
        bot.send_message(call.from_user.id,
                         text=text_.instruction('eng'),
                         reply_markup=keybaord.menu('eng'))
        db.update_language(call.from_user.id, 'eng')

'''
@bot.message_handler(commands=["geo"])
def geo(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_geo = types.KeyboardButton(text=f'{emoji.GLOBE_SHOWING_AMERICAS}{emoji.ROUND_PUSHPIN}',
                                      request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку и передай мне свое местоположение", reply_markup=keyboard)
'''

@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        '''
        photo_generator(user_id=message.from_user.id,
                        x=message.location.longitude,
                        y=message.location.latitude)
        '''
        bot.get_user_profile_photos(message.chat.id)
        print("широта(y): %s; долгота(x): %s" % (message.location.latitude, message.location.longitude))

bot.polling()