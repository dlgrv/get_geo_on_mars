from config import token
import emoji
import telebot
from photo_generator import create_map_with_geotag
import db
import keybaord
import text_
from photo_generator import ava_resize

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
            ava_resize(message.chat.id)
            return True
        except Exception as e:
            print('Error from save_user_profile_photo: ', e)
            return False
    else:
        return False

if __name__ == '__main__':
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
            bot.send_message(message.chat.id,
                             text='Запускаем ракету!')
            save_user_profile_photo(message)
            create_map_with_geotag(uid=message.from_user.id,
                                   gradus_x=message.location.longitude,
                                   gradus_y=message.location.latitude)
            uid = message.chat.id
            map_with_geotag = open(f'./ready_map_for_user/{uid}.jpg', 'rb')
            bot.send_photo(message.chat.id, map_with_geotag)
            bot.send_message(message.chat.id, f'{message.location.longitude}, {message.location.latitude}')

    bot.polling()