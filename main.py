from config import token
import emoji
import telebot
import photo_generator
import db
import keybaord
import text_
from photo_generator import ava_resize
from info_from_wikipedia import get_info

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
                             text=text_.instruction(call.data),
                             reply_markup=keybaord.menu('rus'))
            db.update_language(call.from_user.id, 'rus')
        elif call.data == 'eng':
            bot.answer_callback_query(call.id, f'Language selected{emoji.CHECK_MARK_BUTTON}')
            bot.send_message(call.from_user.id,
                             text=text_.instruction(call.data),
                             reply_markup=keybaord.menu('eng'))
            db.update_language(call.from_user.id, 'eng')

    @bot.message_handler(content_types=["location"])
    def location(message):
        if message.location is not None:
            bot.delete_message(message.chat.id, message.id)
            lang = db.get_language(message.chat.id)[0]
            if lang == 'rus':
                bot.send_message(message.chat.id,
                                 text=f'{emoji.ROCKET}Запускаем ракету!\n'
                                      f'Пожалуйста, ожидайте...')
            elif lang == 'eng':
                bot.send_message(message.chat.id,
                                 text=f'{emoji.ROCKET}Launch the rocket!\n'
                                      f'Please wait...')
            save_user_profile_photo(message)
            nearest_attraction_id = photo_generator.search_nearest_attraction(uid=message.from_user.id,
                                                                              gradus_x=message.location.longitude,
                                                                              gradus_y=message.location.latitude)
            uid = message.chat.id
            map_with_geotag = open(f'./ready_map_for_user/{uid}.jpg', 'rb')
            bot.send_photo(message.chat.id, map_with_geotag)
            bot.send_message(message.chat.id, text=text_.info_about(lang, nearest_attraction_id))

    bot.polling()