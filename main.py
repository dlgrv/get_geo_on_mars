from config import token
import emoji
import telebot
import photo_generator
import db
import keybaord
import text_
from photo_generator import ava_resize
import time

bot = telebot.TeleBot(token)

# КОД ИМЕЕТ ТУПОЙ КОПИПАСТ ЦЕЛЫХ ФУНКЦИЙ В 2-УХ МЕСТАХ, ПИСАЛ НА ХОДУ, ДОЙДУТ РУКИ- ИСПРАВЛЮ

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
        uid = call.from_user.id
        if call.data == 'rus':
            bot.answer_callback_query(call.id, f'Язык выбран{emoji.CHECK_MARK_BUTTON}')
            bot.send_message(chat_id=uid,
                             text=text_.instruction(call.data),
                             reply_markup=keybaord.menu('rus'))
            db.update_language(uid, 'rus')
        elif call.data == 'eng':
            bot.answer_callback_query(call.id, f'Language selected{emoji.CHECK_MARK_BUTTON}')
            bot.send_message(chat_id=uid,
                             text=text_.instruction(call.data),
                             reply_markup=keybaord.menu('eng'))
            db.update_language(uid, 'eng')

    time_limit_for_location = 12
    location_timer = {}
    @bot.message_handler(content_types=["location"])
    def location(message):
        uid = message.chat.id
        lang = db.get_language(uid=uid)[0]
        real_time = time.time()
        bot.delete_message(chat_id=uid,
                           message_id=message.id)
        if message.location is not None:
            if uid not in location_timer:
                location_timer[uid] = real_time
                if lang == 'rus':
                    bot.send_message(chat_id=uid,
                                     text=f'{emoji.ROCKET}Запускаем ракету!\n'
                                          f'{emoji.MAN_BOWING_LIGHT_SKIN_TONE}Пожалуйста, ожидайте...')
                elif lang == 'eng':
                    bot.send_message(chat_id=uid,
                                     text=f'{emoji.ROCKET}Launch the rocket!\n'
                                          f'{emoji.MAN_BOWING_LIGHT_SKIN_TONE}Please wait...')
                save_user_profile_photo(message)
                nearest_attraction_id = photo_generator.search_nearest_attraction(uid=message.from_user.id,
                                                                                  gradus_x=message.location.longitude,
                                                                                  gradus_y=message.location.latitude)
                map_with_geotag = open(f'./ready_map_for_user/{uid}.jpg', 'rb')
                bot.send_photo(chat_id=message.chat.id,
                               photo=map_with_geotag)
                bot.send_message(chat_id=message.chat.id,
                                 text=text_.info_about(lang, nearest_attraction_id))
                db.add_info_about_geo(uid=uid,
                                      gradus_x=message.location.longitude,
                                      gradus_y=message.location.latitude)
            elif time.time() - location_timer[uid] > time_limit_for_location:
                location_timer[uid] = real_time
                if lang == 'rus':
                    bot.send_message(chat_id=uid,
                                     text=f'{emoji.ROCKET}Запускаем ракету!\n'
                                          f'{emoji.MAN_BOWING_LIGHT_SKIN_TONE}Пожалуйста, ожидайте...')
                elif lang == 'eng':
                    bot.send_message(chat_id=uid,
                                     text=f'{emoji.ROCKET}Launch the rocket!\n'
                                          f'{emoji.MAN_BOWING_LIGHT_SKIN_TONE}Please wait...')
                save_user_profile_photo(message)
                nearest_attraction_id = photo_generator.search_nearest_attraction(uid=message.from_user.id,
                                                                                  gradus_x=message.location.longitude,
                                                                                  gradus_y=message.location.latitude)
                map_with_geotag = open(f'./ready_map_for_user/{uid}.jpg', 'rb')
                bot.send_photo(chat_id=message.chat.id,
                               photo=map_with_geotag)
                bot.send_message(chat_id=message.chat.id,
                                 text=text_.info_about(lang, nearest_attraction_id))
                db.add_info_about_geo(uid=uid,
                                      gradus_x=message.location.longitude,
                                      gradus_y=message.location.latitude)
            else:
                if lang == 'rus':
                    bot.send_message(chat_id=uid,
                                     text=f'{emoji.WARNING}Нельзя запрашивать свое местоположение чаще одного раза '
                                          f'в {time_limit_for_location} секунд')
                elif lang == 'eng':
                    bot.send_message(chat_id=uid,
                                     text=f"{emoji.WARNING}You can't request your location more than once every "
                                          f"{time_limit_for_location} seconds")
        '''
        else:
            if lang == 'rus':
                bot.send_message(chat_id=uid,
                                 text='Не удалось определwsvить ваше местоположение')
            elif lang == 'eng':
                bot.send_message(chat_id=uid,
                                 text="Couldn't determine your location")
        '''

    list_timer = {}
    time_limit_for_list = 5
    @bot.message_handler(content_types=['text'])
    def send_text(message):
        uid = message.chat.id
        real_time = time.time()
        try:
            if message.text == f'{emoji.WORLD_MAP}Список моих мест{emoji.MEMO}':
                bot.delete_message(message.chat.id, message.id)
                lang = 'rus'
                if uid not in list_timer:
                    list_timer[uid] = real_time
                    bot.send_message(message.chat.id,
                                     text=text_.get_attractions_list(uid=message.chat.id,
                                                                     lang=lang))
                elif real_time - list_timer[uid] > time_limit_for_list:
                    list_timer[uid] = real_time
                    bot.send_message(chat_id=message.chat.id,
                                     text=text_.get_attractions_list(uid=message.chat.id,
                                                                     lang=lang))
                else:
                    bot.send_message(chat_id=message.chat.id,
                                     text=f'{emoji.WARNING}Нельзя запрашивать список своих мест чаще одного раза '
                                          f'в {time_limit_for_list} секунд')
            elif message.text == f"{emoji.WORLD_MAP}List of my places{emoji.MEMO}":
                bot.delete_message(message.chat.id, message.id)
                lang = 'eng'
                if uid not in list_timer:
                    list_timer[uid] = real_time
                    bot.send_message(message.chat.id,
                                     text=text_.get_attractions_list(uid=message.chat.id,
                                                                     lang=lang))
                elif real_time - list_timer[uid] > time_limit_for_list:
                    list_timer[uid] = real_time
                    bot.send_message(chat_id=message.chat.id,
                                     text=text_.get_attractions_list(uid=message.chat.id,
                                                                     lang=lang))
                else:
                    bot.send_message(message.chat.id,
                                     text=f"{emoji.WARNING}You can't request list of your places more than once"
                                          f" every {time_limit_for_list} seconds")
        except Exception as e:
            print('Error from get attraction list: ', e)

    bot.polling()